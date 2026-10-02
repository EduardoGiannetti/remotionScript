"""Servidor MCP que transcreve músicas com WhisperX e gera o JSON de comentários do Remotion.

Fluxo de `transcribe_audio`:
1. transcreve o áudio (WhisperX) e alinha cada palavra no tempo (wav2vec2);
2. localiza na transcrição cada frase da letra de `timestamps/`, aceitando repetições,
   frases puladas e fora de ordem, já que músicas de IA não seguem a letra à risca;
3. realinha o texto exato da letra em cada trecho encontrado, para timestamps precisos;
4. associa cada frase cantada ao comentário de origem e grava `comments/comments.json`.

Uso:
    python whisper_mcp_server.py                      # servidor MCP (stdio)
    python whisper_mcp_server.py <audio.mp3> [--lyrics <arquivo>]   # execução direta
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import re
import shutil
import sys
import subprocess
import threading
import unicodedata
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any, Iterator

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

PROJECT_DIR = Path(__file__).resolve().parent
TIMESTAMPS_DIR = PROJECT_DIR / "timestamps"
ALIGNED_DIR = TIMESTAMPS_DIR / "aligned"
COMMENTS_DIR = PROJECT_DIR / "comments"
COMMENTS_OUTPUT = COMMENTS_DIR / "comments.json"
PUBLIC_DIR = PROJECT_DIR / "public"
PUBLIC_AUDIO_DIR = PUBLIC_DIR / "audio"
RENDER_OUTPUT_DIR = PROJECT_DIR / "out"

WHISPER_MODEL = os.environ.get("WHISPER_MODEL", "medium")
DEVICE = "cpu"
COMPUTE_TYPE = "int8"
LANGUAGE = "pt"
SAMPLE_RATE = 16000  # whisperx.load_audio sempre reamostra para 16 kHz

MIN_LINE_SIMILARITY = 0.6  # frase da letra x trecho transcrito
MIN_SHORT_LINE_SIMILARITY = 0.75  # frases curtas casam com ruído com mais facilidade
SHORT_LINE_CHARS = 12
MIN_COMMENT_SIMILARITY = 0.6  # frase da letra x texto do comentário
REFINE_PADDING_SECONDS = 1.5  # folga em torno do trecho do ASR no realinhamento

log = logging.getLogger("whisperx-lyrics")
mcp = MCPServer("whisperx-lyrics-aligner")
_models: dict[str, Any] = {}
# Uma execução por vez: os modelos são compartilhados e todas gravam o mesmo comments.json.
_run_lock = threading.Lock()


@mcp.tool()
def transcribe_audio(
    file_path: str,
    lyrics_path: str | None = None,
    comments_path: str | None = None,
    fps: int = 30,
    hold_seconds: float = 1.5,
    use_template_background: bool = True,
    loop_background: bool = True,
) -> dict[str, Any]:
    """Transcreve uma música, sincroniza as frases da letra e gera comments/comments.json.

    Args:
        file_path: caminho do MP3 da música.
        lyrics_path: JSON da letra (caminho, nome em timestamps/ ou task_id). Se omitido,
            usa a letra cujo task_id aparece no nome do áudio ou, na falta dele, a letra
            de timestamps/ que melhor corresponde ao que foi cantado.
        comments_path: JSON de comentários de origem. Padrão: o mais recente em comments/.
        fps: FPS da composição do Remotion.
        hold_seconds: tempo extra que o comentário fica na tela após o fim da frase
            (limitado pelo início da frase seguinte).
        use_template_background: depois do vídeo original, usa um vídeo template (sempre em
            loop) como fundo dos comentários em vez do vídeo original.
        loop_background: com o vídeo original de fundo, True o repete em loop e False deixa
            um frame estático dele. Ignorado quando use_template_background é True.
    """
    with _run_lock:
        try:
            return _run(
                _clean_path(file_path) or "",
                _clean_path(lyrics_path),
                _clean_path(comments_path),
                fps,
                hold_seconds,
                use_template_background,
                loop_background,
            )
        except subprocess.CalledProcessError as error:
            raise ToolError(f"Falha ao renderizar o vídeo (código {error.returncode}).") from error
        except (OSError, ValueError) as error:
            # Sem ToolError, o SDK esconde a mensagem e o cliente só vê "Error executing tool".
            raise ToolError(str(error)) from error


def _clean_path(value: str | None) -> str | None:
    """Tira espaços e aspas que vêm junto ao colar um caminho ("C:\\...mp3")."""
    cleaned = (value or "").strip().strip("\"'").strip()
    return cleaned or None


def _run(
    file_path: str,
    lyrics_path: str | None,
    comments_path: str | None,
    fps: int,
    hold_seconds: float,
    use_template_background: bool,
    loop_background: bool,
) -> dict[str, Any]:
    audio_path = _resolve_audio(file_path)
    lyrics_candidates = _lyrics_candidates(audio_path, lyrics_path)
    comments_source, comments = _load_comments(comments_path)

    whisperx = _whisperx()
    audio = whisperx.load_audio(str(audio_path))
    duration = len(audio) / SAMPLE_RATE

    log.info("Transcrevendo %s (%.1fs) com o modelo %s", audio_path.name, duration, WHISPER_MODEL)
    asr_text, words = _transcribe_words(audio)
    lyrics_file, lines, located = _pick_lyrics(lyrics_candidates, words)
    log.info("Letra: %s (%d frases encontradas)", lyrics_file.name, len(located))

    phrases = [
        {
            "line": match["line"],
            "lyric": lines[match["line"]],
            "asrText": " ".join(w["word"] for w in words[match["first"] : match["last"] + 1]),
            "asrStart": words[match["first"]]["start"],
            "asrEnd": words[match["last"]]["end"],
            "similarity": round(match["similarity"], 3),
        }
        for match in located
    ]
    _refine_timestamps(phrases, audio, duration)
    _assign_frames(phrases, fps, hold_seconds, duration)

    matches = {index: _match_comment(lines[index], comments) for index in {p["line"] for p in phrases}}
    entries: list[dict[str, Any]] = []
    unmatched: list[dict[str, Any]] = []
    for phrase in phrases:
        comment, score = matches[phrase["line"]]
        phrase["commentSimilarity"] = round(score, 3)
        if comment is None or score < MIN_COMMENT_SIMILARITY:
            unmatched.append(phrase)
            continue
        phrase["username"] = (
            (comment.get("author") or {}).get("username")
            or comment.get("username")
            or comment.get("uniqueId")  # TikTok
        )
        entries.append(
            {
                **comment,
                "startFrame": phrase["startFrame"],
                "durationInFrames": phrase["durationInFrames"],
            }
        )
    if not entries:
        # Não sobrescreve o comments.json atual com um vídeo sem comentários.
        raise ValueError(
            f"Nenhuma frase de {lyrics_file.name} foi associada a um comentário. "
            f"Transcrição: {asr_text[:300]}"
        )

    remotion_audio_path = _publish_audio(audio_path)
    _write_json(
        COMMENTS_OUTPUT,
        {
            "comments": entries,
            "audioPath": remotion_audio_path,
            "fps": fps,
            "audioDurationInFrames": round(duration * fps),
        },
    )

    sung_lines = {p["line"] for p in phrases}
    skipped_lyrics = [line for index, line in enumerate(lines) if index not in sung_lines]
    alignment_path = ALIGNED_DIR / f"{audio_path.stem}.json"
    _write_json(
        alignment_path,
        {
            "audio": str(audio_path),
            "audioPath": remotion_audio_path,
            "lyricsFile": str(lyrics_file),
            "commentsSource": str(comments_source),
            "duration": round(duration, 3),
            "fps": fps,
            "model": WHISPER_MODEL,
            "transcript": asr_text,
            "phrases": phrases,
            "skippedLyrics": skipped_lyrics,
            "words": words,
        },
    )
    for phrase in unmatched:
        log.warning("Frase sem comentário correspondente: %s", phrase["lyric"])

    # O template só existe em loop: template + imagem estática não é uma saída válida.
    loop_background = loop_background or use_template_background
    # video_path = _render_video(
    #     audio_path,
    #     {"useTemplateBackground": use_template_background, "loopBackground": loop_background},
    # )
    video_path = None  # renderização desativada temporariamente

    return {
        "videoPath": str(video_path),
        "useTemplateBackground": use_template_background,
        "loopBackground": loop_background,
        "commentsJson": str(COMMENTS_OUTPUT),
        "alignmentJson": str(alignment_path),
        "audioPath": remotion_audio_path,
        "lyricsFile": lyrics_file.name,
        "commentsSource": comments_source.name,
        "durationSeconds": round(duration, 3),
        "phrases": [
            {
                "text": p["lyric"],
                "start": p["start"],
                "end": p["end"],
                "startFrame": p["startFrame"],
                "durationInFrames": p["durationInFrames"],
                "username": p.get("username"),
            }
            for p in phrases
        ],
        "skippedLyrics": skipped_lyrics,
        "unmatchedPhrases": [p["lyric"] for p in unmatched],
    }


# --- Entradas ----------------------------------------------------------------------------


def _resolve_audio(file_path: str) -> Path:
    path = Path(file_path).expanduser()
    options = [path] if path.is_absolute() else [PROJECT_DIR / path, PUBLIC_DIR / path]
    for option in options:
        if option.is_file():
            return option.resolve()
    raise FileNotFoundError(f"Arquivo de áudio não encontrado: {file_path}")


def _lyrics_candidates(audio_path: Path, lyrics_path: str | None) -> list[Path]:
    if lyrics_path:
        path = Path(lyrics_path).expanduser()
        options = (
            [path]
            if path.is_absolute()
            else [TIMESTAMPS_DIR / path, PROJECT_DIR / path, TIMESTAMPS_DIR / f"{lyrics_path}_lyrics.json"]
        )
        for option in options:
            if option.is_file():
                return [option.resolve()]
        raise FileNotFoundError(f"Letra não encontrada: {lyrics_path}")

    candidates = sorted(
        TIMESTAMPS_DIR.glob("*_lyrics.json"), key=lambda p: p.stat().st_mtime, reverse=True
    )
    if not candidates:
        raise FileNotFoundError(f"Nenhuma letra (*_lyrics.json) encontrada em {TIMESTAMPS_DIR}")

    # Áudios salvos como musica_<task_id[:8]>_N.mp3 identificam a letra pelo nome.
    for candidate in candidates:
        task_prefix = candidate.name.split("-")[0]
        if len(task_prefix) >= 8 and task_prefix in audio_path.stem:
            return [candidate]
    return candidates


def _read_lyric_lines(lyrics_path: Path) -> list[str]:
    """Lê as frases da letra, ignorando marcações de seção como [Chorus]."""
    data = json.loads(lyrics_path.read_text(encoding="utf-8"))
    raw_lines: Any = data.get("text") if isinstance(data, dict) else data
    if not raw_lines and isinstance(data, dict):
        raw_lines = (data.get("payload_completo") or {}).get("lyrics", "")
    if isinstance(raw_lines, str):
        raw_lines = raw_lines.splitlines()

    lines: list[str] = []
    seen: set[str] = set()
    for raw_line in raw_lines or []:
        line = str(raw_line).strip()
        key = _match_key(line)
        if key and not re.fullmatch(r"\[[^\]]*\]", line) and key not in seen:
            seen.add(key)
            lines.append(line)
    if not lines:
        raise ValueError(f"Nenhuma frase encontrada na letra: {lyrics_path}")
    return lines


def _load_comments(comments_path: str | None) -> tuple[Path, list[dict[str, Any]]]:
    if comments_path:
        path = Path(comments_path).expanduser()
        if not path.is_absolute():
            path = next(
                (p for p in (COMMENTS_DIR / path, PROJECT_DIR / path) if p.is_file()),
                COMMENTS_DIR / path,
            )
    else:
        # comentarios-AAAAMMDD_HHMMSS.json: a ordem alfabética é a cronológica.
        sources = sorted(p for p in COMMENTS_DIR.glob("*.json") if p.name != COMMENTS_OUTPUT.name)
        if not sources:
            raise FileNotFoundError(f"Nenhum arquivo de comentários encontrado em {COMMENTS_DIR}")
        path = sources[-1]
    if not path.is_file():
        raise FileNotFoundError(f"Arquivo de comentários não encontrado: {path}")

    data = json.loads(path.read_text(encoding="utf-8"))
    comments = data if isinstance(data, list) else data.get("comments", [])
    return path, [c for c in comments if isinstance(c, dict) and _comment_text(c).strip()]


def _publish_audio(audio_path: Path) -> str:
    """Copia o áudio para public/audio/ e retorna o caminho usado por staticFile()."""
    PUBLIC_AUDIO_DIR.mkdir(parents=True, exist_ok=True)
    target = PUBLIC_AUDIO_DIR / audio_path.name
    if target.resolve() != audio_path:
        shutil.copy2(audio_path, target)
    return f"audio/{target.name}"


def _write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def _render_video(audio_path: Path, props: dict[str, Any]) -> Path:
    """Exporta a composição usando o comments.json recém-gerado."""
    RENDER_OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    safe_stem = re.sub(r"[^A-Za-z0-9._-]+", "_", audio_path.stem).strip("._") or "video"
    output_path = RENDER_OUTPUT_DIR / f"{safe_stem}.mp4"
    command = [
        "npx",
        "remotion",
        "render",
        "src/index.ts",
        "InstagramCommentVideo",
        str(output_path.relative_to(PROJECT_DIR)),
    ]
    # A escolha do fundo vai por variáveis REMOTION_* (lidas no Composition.tsx), porque
    # JSON em --props na linha de comando quebra nas aspas do cmd.exe.
    env = {
        **os.environ,
        "REMOTION_USE_TEMPLATE_BACKGROUND": str(props["useTemplateBackground"]).lower(),
        "REMOTION_LOOP_BACKGROUND": str(props["loopBackground"]).lower(),
    }
    log.info("Renderizando vídeo para %s com %s", output_path, props)
    if os.name == "nt":
        subprocess.run(
            subprocess.list2cmdline(command),
            cwd=PROJECT_DIR,
            check=True,
            shell=True,
            env=env,
            stdout=subprocess.DEVNULL,
        )
    else:
        subprocess.run(command, cwd=PROJECT_DIR, check=True, env=env, stdout=subprocess.DEVNULL)
    log.info("Vídeo exportado: %s", output_path)
    return output_path


# --- WhisperX ----------------------------------------------------------------------------


def _whisperx() -> Any:
    import whisperx  # import tardio: carregar torch leva alguns segundos

    return whisperx


def _asr_model() -> Any:
    if "asr" not in _models:
        _models["asr"] = _whisperx().load_model(
            WHISPER_MODEL,
            DEVICE,
            compute_type=COMPUTE_TYPE,
            language=LANGUAGE,
            threads=os.cpu_count() or 4,
        )
    return _models["asr"]


def _align_model() -> tuple[Any, dict[str, Any]]:
    if "align" not in _models:
        _models["align"] = _whisperx().load_align_model(language_code=LANGUAGE, device=DEVICE)
    return _models["align"]


def _transcribe_words(audio: Any) -> tuple[str, list[dict[str, Any]]]:
    """Transcreve o áudio e devolve o texto e as palavras com início/fim em segundos."""
    result = _asr_model().transcribe(audio, batch_size=8, language=LANGUAGE)
    align_model, metadata = _align_model()
    aligned = _whisperx().align(result["segments"], align_model, metadata, audio, DEVICE)

    words: list[dict[str, Any]] = []
    for item in aligned["word_segments"]:
        # Palavras sem caracteres alinháveis herdam o tempo da anterior.
        start = float(item.get("start", words[-1]["end"] if words else 0.0))
        end = float(item.get("end", start))
        words.append({"word": item["word"], "start": round(start, 3), "end": round(max(start, end), 3)})
    text = " ".join(segment["text"].strip() for segment in result["segments"])
    return text, words


def _refine_timestamps(phrases: list[dict[str, Any]], audio: Any, duration: float) -> None:
    """Realinha o texto exato da letra em torno de cada trecho achado pelo ASR.

    O ASR às vezes não reconhece o começo ou o fim da frase ("fura" em vez de
    "furadeira"); o alinhamento forçado com a letra recupera esse pedaço. A janela
    nunca invade as frases vizinhas.
    """
    whisperx = _whisperx()
    align_model, metadata = _align_model()
    for index, phrase in enumerate(phrases):
        previous_end = phrases[index - 1]["asrEnd"] if index else 0.0
        next_start = phrases[index + 1]["asrStart"] if index + 1 < len(phrases) else duration
        window_start = min(phrase["asrStart"], max(previous_end, phrase["asrStart"] - REFINE_PADDING_SECONDS))
        window_end = max(phrase["asrEnd"], min(next_start, phrase["asrEnd"] + REFINE_PADDING_SECONDS))

        aligned = whisperx.align(
            [{"start": window_start, "end": window_end, "text": " ".join(_spoken_words(phrase["lyric"]))}],
            align_model,
            metadata,
            audio,
            DEVICE,
        )
        times = [
            (float(word["start"]), float(word["end"]))
            for word in aligned["word_segments"]
            if "start" in word and "end" in word
        ]
        start = min((t[0] for t in times), default=phrase["asrStart"])
        end = max((t[1] for t in times), default=phrase["asrEnd"])
        phrase["alignedStart"], phrase["alignedEnd"] = round(start, 3), round(end, 3)
        # O realinhamento só amplia o trecho do ASR. Quando a escrita difere da pronúncia
        # ("GTA 6") ou o ASR tem pouca confiança, o alinhamento forçado tende a comprimir
        # a frase; comparado a timestamps independentes, o início do ASR foi mais confiável.
        phrase["start"] = round(min(phrase["asrStart"], start), 3)
        phrase["end"] = round(max(phrase["asrEnd"], end), 3)


def _assign_frames(
    phrases: list[dict[str, Any]], fps: int, hold_seconds: float, duration: float
) -> None:
    """O comentário aparece no início da frase e sai `hold_seconds` após o fim dela,
    ou antes, quando a próxima frase começa."""
    phrases.sort(key=lambda p: p["start"])
    hold_frames = round(hold_seconds * fps)
    total_frames = round(duration * fps)
    for index, phrase in enumerate(phrases):
        start_frame = round(phrase["start"] * fps)
        limit = round(phrases[index + 1]["start"] * fps) if index + 1 < len(phrases) else total_frames
        end_frame = min(round(phrase["end"] * fps) + hold_frames, limit)
        phrase["startFrame"] = start_frame
        phrase["durationInFrames"] = max(1, end_frame - start_frame)


# --- Letra x transcrição -----------------------------------------------------------------


def _pick_lyrics(
    candidates: list[Path], words: list[dict[str, Any]]
) -> tuple[Path, list[str], list[dict[str, Any]]]:
    """Escolhe, entre as letras candidatas, a que melhor explica o que foi cantado."""
    lyrics: dict[Path, list[str]] = {}
    for path in candidates:
        try:
            lyrics[path] = _read_lyric_lines(path)
        except (OSError, ValueError) as error:
            if len(candidates) == 1:
                raise
            log.warning("Letra ignorada (%s): %s", path.name, error)
    if not lyrics:
        raise ValueError(f"Nenhuma letra válida encontrada em {TIMESTAMPS_DIR}")

    # Pré-filtro barato por vocabulário antes da comparação completa.
    sung = {_fold(w) for word in words for w in _spoken_words(word["word"])}
    shortlist = sorted(
        lyrics,
        key=lambda p: len(sung & {_fold(w) for line in lyrics[p] for w in _spoken_words(line)}),
        reverse=True,
    )[:3]

    best: tuple[float, Path, list[dict[str, Any]]] | None = None
    for path in shortlist:
        located, score = _locate_lines(lyrics[path], words)
        if best is None or score > best[0]:
            best = (score, path, located)
    assert best is not None
    return best[1], lyrics[best[1]], best[2]


def _locate_lines(lines: list[str], words: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], float]:
    """Encontra onde cada frase da letra foi cantada, em qualquer ordem e quantidade.

    Cada frase é comparada letra a letra (sem espaços e acentos) com todos os trechos da
    transcrição que começam e terminam em fronteiras de palavra, o que tolera erros comuns
    do ASR em música ("microondas" -> "micro ondas", "Kazaa" -> "casa"). Depois, uma
    programação dinâmica escolhe o conjunto de trechos sem sobreposição que cobre o
    máximo de letras.
    """
    text_parts: list[str] = []
    starts: dict[int, int] = {}  # posição no texto -> palavra que começa ali
    ends: dict[int, int] = {}  # posição no texto -> palavra que termina ali
    position = 0
    for index, word in enumerate(words):
        key = _match_key(word["word"])
        if not key:
            continue
        starts[position] = index
        text_parts.append(key)
        position += len(key)
        ends[position] = index
    text = "".join(text_parts)

    by_last_word: dict[int, list[dict[str, Any]]] = {}
    for line_index, line in enumerate(lines):
        pattern = _match_key(line)
        min_similarity = MIN_SHORT_LINE_SIMILARITY if len(pattern) < SHORT_LINE_CHARS else MIN_LINE_SIMILARITY
        variants = [
            {
                "line": line_index,
                "first": first,
                "last": last,
                "similarity": 1 - cost / len(pattern),
                # Erros pesam em dobro: trechos com menos de 50% de acerto pontuam
                # negativo, então a frase não é partida em pedaços para somar pontos.
                "score": len(pattern) - 2 * cost,
            }
            for (first, last), cost in _line_variants(pattern, text, starts, ends).items()
        ]
        anchors = [v for v in variants if v["similarity"] >= min_similarity]
        for variant in variants:
            # Variantes um pouco abaixo do limite ficam disponíveis quando sobrepõem uma
            # ocorrência aceita: evita que a frase "engula" uma palavra da frase vizinha
            # só para passar do limite.
            if variant["similarity"] >= min_similarity or (
                variant["similarity"] >= min_similarity - 0.2
                and any(a["first"] <= variant["last"] and variant["first"] <= a["last"] for a in anchors)
            ):
                by_last_word.setdefault(variant["last"], []).append(variant)

    # best[w]: maior pontuação usando apenas as palavras anteriores a w.
    best = [0.0] * (len(words) + 1)
    choice: list[dict[str, Any] | None] = [None] * (len(words) + 1)
    for index in range(len(words)):
        best[index + 1] = best[index]
        for candidate in by_last_word.get(index, []):
            total = best[candidate["first"]] + candidate["score"]
            if total > best[index + 1]:
                best[index + 1], choice[index + 1] = total, candidate

    located: list[dict[str, Any]] = []
    index = len(words)
    while index > 0:
        candidate = choice[index]
        if candidate is None:
            index -= 1
        else:
            located.append(candidate)
            index = candidate["first"]
    located.reverse()
    return located, best[-1]


def _line_variants(
    pattern: str, text: str, starts: dict[int, int], ends: dict[int, int]
) -> dict[tuple[int, int], int]:
    """Custo de edição de cada trecho (primeira palavra, última palavra) para a frase.

    A busca direta dá o melhor início para cada fim; a busca no texto invertido dá o
    melhor fim para cada início. Juntas, permitem recortar as bordas do trecho.
    """
    size = len(text)
    reversed_starts = {size - position: word for position, word in ends.items()}
    reversed_ends = {size - position: word for position, word in starts.items()}
    variants: dict[tuple[int, int], int] = {}
    for start, end, cost in _approximate_matches(pattern, text, starts, ends):
        key = (starts[start], ends[end])
        variants[key] = min(cost, variants.get(key, cost))
    for start, end, cost in _approximate_matches(pattern[::-1], text[::-1], reversed_starts, reversed_ends):
        key = (reversed_ends[end], reversed_starts[start])
        variants[key] = min(cost, variants.get(key, cost))
    return variants


def _approximate_matches(
    pattern: str, text: str, starts: dict[int, int], ends: dict[int, int]
) -> Iterator[tuple[int, int, int]]:
    """Distância de edição entre `pattern` e os trechos de `text` (algoritmo de Sellers).

    Gera (início, fim, custo) para cada fim de palavra, com o melhor início possível.
    """
    size = len(pattern)
    # Coluna j = texto consumido até a posição j; linha i = letras da frase já casadas.
    previous_cost = list(range(size + 1))
    previous_origin = [0] * (size + 1)
    for column in range(1, len(text) + 1):
        char = text[column - 1]
        if column in starts:
            # Um trecho pode começar de graça onde começa uma palavra.
            cost, origin = [0], [column]
        else:
            cost, origin = [previous_cost[0] + 1], [previous_origin[0]]
        for row in range(1, size + 1):
            best = previous_cost[row - 1] + (pattern[row - 1] != char)
            best_origin = previous_origin[row - 1]
            if previous_cost[row] + 1 < best:
                best, best_origin = previous_cost[row] + 1, previous_origin[row]
            if cost[row - 1] + 1 < best:
                best, best_origin = cost[row - 1] + 1, origin[row - 1]
            cost.append(best)
            origin.append(best_origin)
        if column in ends:
            yield origin[size], column, cost[size]
        previous_cost, previous_origin = cost, origin


def _match_comment(line: str, comments: list[dict[str, Any]]) -> tuple[dict[str, Any] | None, float]:
    """Acha o comentário que deu origem à frase (a letra pode perder emojis e acentos)."""
    key = _match_key(line)
    best: dict[str, Any] | None = None
    best_rank = (0.0, 0)
    for comment in comments:
        comment_key = _match_key(_comment_text(comment))
        if not comment_key:
            continue
        score = SequenceMatcher(None, key, comment_key, autojunk=False).ratio()
        if len(key) >= SHORT_LINE_CHARS and key in comment_key:
            score = max(score, 0.95)  # a letra usou só parte do comentário
        rank = (round(score, 3), _likes(comment))  # empate: comentário mais curtido
        if rank > best_rank:
            best, best_rank = comment, rank
    return best, best_rank[0]


def _comment_text(comment: dict[str, Any]) -> str:
    return str(comment.get("text") or comment.get("commentText") or "")


def _likes(comment: dict[str, Any]) -> int:
    try:
        return int(comment.get("likes") or comment.get("diggCount") or 0)  # diggCount: TikTok
    except (TypeError, ValueError):
        return 0


# --- Normalização de texto ---------------------------------------------------------------

_UNITS = (
    "zero um dois tres quatro cinco seis sete oito nove dez onze doze treze catorze "
    "quinze dezesseis dezessete dezoito dezenove"
).split()
_TENS = ("", "", "vinte", "trinta", "quarenta", "cinquenta", "sessenta", "setenta", "oitenta", "noventa")
_HUNDREDS = (
    "", "cento", "duzentos", "trezentos", "quatrocentos",
    "quinhentos", "seiscentos", "setecentos", "oitocentos", "novecentos",
)


def _number_to_words(number: int) -> str:
    """Número por extenso (pt-BR), como é cantado: 300 -> "trezentos"."""
    if number < 20:
        return _UNITS[number]
    if number < 100:
        tens, unit = divmod(number, 10)
        return _TENS[tens] + (f" e {_UNITS[unit]}" if unit else "")
    if number == 100:
        return "cem"
    if number < 1000:
        hundreds, rest = divmod(number, 100)
        return _HUNDREDS[hundreds] + (f" e {_number_to_words(rest)}" if rest else "")
    if number < 1_000_000:
        thousands, rest = divmod(number, 1000)
        head = "mil" if thousands == 1 else f"{_number_to_words(thousands)} mil"
        return head + (f" e {_number_to_words(rest)}" if rest else "")
    return " ".join(_UNITS[int(digit)] for digit in str(number))


def _spoken_words(text: str) -> list[str]:
    """Palavras como são cantadas: minúsculas, sem pontuação/emojis e números por extenso."""
    text = re.sub(r"\d+", lambda m: f" {_number_to_words(int(m.group()))} ", text.lower())
    return re.findall(r"[^\W\d_]+", text)


def _fold(text: str) -> str:
    """Remove acentos: a letra gerada às vezes vem sem acentuação ("cirurgica")."""
    return "".join(c for c in unicodedata.normalize("NFD", text) if not unicodedata.combining(c))


def _match_key(text: str) -> str:
    return _fold("".join(_spoken_words(text)))


def _main() -> None:
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(encoding="utf-8", errors="replace")  # console do Windows é cp1252
    logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(asctime)s %(message)s")

    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("audio", nargs="?", help="MP3 da música; sem ele, inicia o servidor MCP")
    parser.add_argument("--lyrics", help="JSON da letra (padrão: detectado em timestamps/)")
    parser.add_argument("--comments", help="JSON de comentários (padrão: o mais recente em comments/)")
    parser.add_argument("--fps", type=int, default=30)
    parser.add_argument("--hold", type=float, default=1.5, help="segundos extras na tela após a frase")
    args = parser.parse_args()

    if args.audio is None:
        mcp.run()
        return
    result = transcribe_audio(args.audio, args.lyrics, args.comments, args.fps, args.hold)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    _main()
