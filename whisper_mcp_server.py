import json
import importlib
import re
import shutil
from pathlib import Path
from typing import Any

from faster_whisper import WhisperModel
# from mcp.server.fastmcp import FastMCP

# mcp = FastMCP("faster-whisper-transcriber")
model = WhisperModel("small", device="cpu", compute_type="int8")

# @mcp.tool()
def transcribe_audio(
    file_path: str,
) -> dict[str, Any]:
    """Transcreve ou alinha um áudio usando o faster-whisper ou o WhisperX."""
    audio_path = Path(file_path).expanduser().resolve()
    if not audio_path.is_file():
        raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_path}")

    project_dir = Path(__file__).parent
    public_audio_dir = project_dir / "public" / "audio"
    public_audio_dir.mkdir(parents=True, exist_ok=True)
    public_audio_path = public_audio_dir / audio_path.name
    shutil.copy2(audio_path, public_audio_path)

    remotion_audio_path = f"audio/{public_audio_path.name}"
    timestamps_dir = project_dir / "timestamps"
    transcript_paths = sorted(
        path for path in timestamps_dir.glob("*.json") if path.name != "transcript.json"
    )
    transcript_path = transcript_paths[-1] if transcript_paths else None
    comments_dir = project_dir / "comments"
    comments_path = comments_dir / "comments.json"
    source_paths = sorted(
        path for path in comments_dir.glob("*.json") if path.name != comments_path.name
    )
    if not source_paths:
        raise FileNotFoundError(
            f"Nenhum arquivo de comentários encontrado em: {comments_dir}"
        )

    source_data = json.loads(source_paths[-1].read_text(encoding="utf-8"))
    comments_data = {"comments": source_data} if isinstance(source_data, list) else source_data
    if not isinstance(comments_data, dict):
        raise ValueError("O arquivo de comentários precisa conter uma lista ou um objeto JSON.")

    comments_data["audioPath"] = remotion_audio_path
    comments_dir.mkdir(parents=True, exist_ok=True)
    comments_path.write_text(
        json.dumps(comments_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    if transcript_path is not None:
        result = _forced_align(
            audio_path=audio_path,
            transcript_path=transcript_path,
        )
        result["audioPath"] = remotion_audio_path
        return result

    segments, info = model.transcribe(
        str(audio_path),
        language="pt",
        task="transcribe",
        word_timestamps=True,
        vad_filter=False,
    )

    transcript_parts: list[str] = []
    all_words = []
    for segment in segments:
        text = segment.text.strip()
        if text:
            transcript_parts.append(text)
        for word in segment.words or []:
            all_words.append(
                {
                    "word": word.word,
                    "start": word.start,
                    "end": word.end,
                    "probability": word.probability,
                }
            )

    return {
        "audioPath": remotion_audio_path,
        "duration": info.duration,
        "transcript": " ".join(transcript_parts),
        "words": all_words,
    }


def _forced_align(audio_path: Path, transcript_path: Path) -> dict[str, Any]:
    """Alinha texto externo ao áudio e retorna timestamps por palavra."""
    if not transcript_path.is_file():
        raise FileNotFoundError(
            f"Arquivo de transcrição não encontrado: {transcript_path}"
        )

    try:
        whisperx = importlib.import_module("whisperx")
    except ImportError as error:
        raise RuntimeError(
            "WhisperX não está instalado. Execute: pip install whisperx"
        ) from error

    external_data = json.loads(transcript_path.read_text(encoding="utf-8"))
    external_segments = external_data.get("segments")
    phrase_texts = _read_phrase_texts(external_data)

    if external_segments:
        alignment_segments = [
            {
                "start": float(segment["start"]),
                "end": float(segment["end"]),
                "text": str(segment["text"]).strip(),
            }
            for segment in external_segments
            if str(segment.get("text", "")).strip()
        ]
        phrase_texts = [segment["text"] for segment in alignment_segments]
    else:
        if not phrase_texts:
            raise ValueError(
                "O JSON externo precisa conter 'phrases', 'lines', 'text' ou 'transcript'."
            )

        audio = whisperx.load_audio(str(audio_path))
        alignment_segments = [
            {
                "start": 0.0,
                "end": len(audio) / 16000,
                "text": " ".join(phrase_texts),
            }
        ]

    audio = whisperx.load_audio(str(audio_path))
    duration = len(audio) / 16000
    device = "cpu"
    language = external_data.get("language", "pt")
    align_model, metadata = whisperx.load_align_model(
        language_code=language,
        device=device,
    )
    aligned = whisperx.align(
        alignment_segments,
        align_model,
        metadata,
        audio,
        device,
        return_char_alignments=False,
    )

    words = [
        {
            "word": word["word"],
            "start": word["start"],
            "end": word["end"],
            "probability": word.get("score"),
        }
        for word in aligned.get("word_segments", [])
        if word.get("start") is not None and word.get("end") is not None
    ]
    phrases = _group_words_into_phrases(phrase_texts, words)

    return {
        "duration": duration,
        "transcript": " ".join(phrase_texts),
        "segments": phrases,
    }


def _read_phrase_texts(external_data: dict[str, Any]) -> list[str]:
    """Lê frases mantendo quebras de linha da letra oficial."""
    phrases = external_data.get("phrases", external_data.get("lines"))
    if phrases is not None:
        if not isinstance(phrases, list):
            raise ValueError("'phrases' ou 'lines' precisa ser uma lista de textos.")
        raw_lines = phrases
    else:
        text = str(external_data.get("text", external_data.get("transcript", "")))
        raw_lines = text.splitlines()

    return [
        line
        for phrase in raw_lines
        if (line := str(phrase).strip())
        and not re.fullmatch(r"\[[^\]]+\]", line)
    ]


def _normalise_words(text: str) -> list[str]:
    return re.findall(r"[\wÀ-ÿ]+", text.casefold())


def _group_words_into_phrases(
    phrase_texts: list[str],
    words: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    """Reconstrói timestamps por frase a partir das palavras alinhadas."""
    aligned_index = 0
    phrases: list[dict[str, Any]] = []

    for phrase_text in phrase_texts:
        expected_words = _normalise_words(phrase_text)
        if not expected_words:
            continue

        phrase_words: list[dict[str, Any]] = []
        expected_index = 0
        while aligned_index < len(words) and expected_index < len(expected_words):
            candidate = _normalise_words(words[aligned_index]["word"])
            aligned_index += 1
            if candidate and candidate[0] == expected_words[expected_index]:
                phrase_words.append(words[aligned_index - 1])
                expected_index += 1

        if expected_index != len(expected_words) or not phrase_words:
            raise ValueError(
                f"Não foi possível localizar a frase completa no alinhamento: {phrase_text}"
            )

        phrases.append(
            {
                "text": phrase_text,
                "start": phrase_words[0]["start"],
                "end": phrase_words[-1]["end"],
            }
        )

    return phrases

if __name__ == "__main__":
    # audio_file = ""
    # if not audio_file:
    #     print("tem nao")
    # else:
        result = transcribe_audio(
            file_path=r"C:\Users\EduardoGiannetti\Downloads\mermaid\downloads\musica_b226fd66_1.mp3",
        )
        output = json.dumps(result, ensure_ascii=False, indent=2)
        output_path = Path(__file__).parent / "timestamps" / "transcript.json"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(output, encoding="utf-8")
        print(output)
