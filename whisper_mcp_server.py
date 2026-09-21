import json
import shutil
from pathlib import Path
from typing import Any

from faster_whisper import WhisperModel
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("faster-whisper-transcriber")
model = WhisperModel("small", device="cpu", compute_type="int8")


@mcp.tool()
def transcribe_audio(file_path: str) -> dict[str, Any]:
    """Transcreve um arquivo de áudio local usando o faster-whisper."""
    audio_path = Path(file_path).expanduser().resolve()
    if not audio_path.is_file():
        raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_path}")

    project_dir = Path(__file__).parent
    public_audio_dir = project_dir / "public" / "audio"
    public_audio_dir.mkdir(parents=True, exist_ok=True)
    public_audio_path = public_audio_dir / audio_path.name
    shutil.copy2(audio_path, public_audio_path)

    remotion_audio_path = f"audio/{public_audio_path.name}"
    comments_path = project_dir / "src" / "comments.json"
    comments_data = json.loads(comments_path.read_text(encoding="utf-8"))
    comments_data["audioPath"] = remotion_audio_path
    comments_path.write_text(
        json.dumps(comments_data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

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


if __name__ == "__main__":
    result = transcribe_audio(
        r"C:\Users\EduardoGiannetti\Downloads\ACE-Step\.cache\acestep\tmp\api_audio\lyric_test.mp3"
    )
    output = json.dumps(result, ensure_ascii=False, indent=2)
    output_path = Path(__file__).parent / "timestamps" / "transcript.json"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(output, encoding="utf-8")
    print(output)
