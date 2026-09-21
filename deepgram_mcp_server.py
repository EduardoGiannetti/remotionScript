import os
from pathlib import Path
from typing import Any

from deepgram import DeepgramClient
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

mcp = FastMCP("DeepgramTranscriber")
load_dotenv(Path(__file__).with_name(".env"))


# @mcp.tool()
def transcribe_audio(file_path: str) -> dict[str, Any]:
	"""Transcreve um arquivo de áudio local usando o Deepgram."""
	api_key = os.getenv("DEEPGRAM_API_KEY")
	if not api_key:
		raise RuntimeError("Defina a variável de ambiente DEEPGRAM_API_KEY antes de executar.")

	audio_path = Path(file_path).expanduser().resolve()
	if not audio_path.is_file():
		raise FileNotFoundError(f"Arquivo de áudio não encontrado: {audio_path}")

	deepgram = DeepgramClient(api_key=api_key)
	with audio_path.open("rb") as file:
		buffer_data = file.read()

	response = deepgram.listen.v1.media.transcribe_file(
		request=buffer_data,
		model="nova-3",
		language="pt",
		punctuate=True,
		smart_format=True,
		utterances=True,
		paragraphs=True,
	)
    
	metadata = getattr(response, "metadata", None)
	duration = getattr(metadata, "duration", 0)
	transcript = ""
	words_list: list[dict[str, Any]] = []
	channels = response.results.channels

	if channels and channels[0].alternatives:
		alternative = channels[0].alternatives[0]
		transcript = alternative.transcript or ""
		words = alternative.words or []
		for word in words:
			words_list.append({
				"word": word.punctuated_word or word.word,
				"start": word.start,
				"end": word.end,
			})
	return {
		"duration": duration,
		"transcript": transcript,
		"words": words_list,
	}


if __name__ == "__main__":
	# mcp.run()
	result = transcribe_audio(
		r"C:\Users\EduardoGiannetti\Downloads\ACE-Step\.cache\acestep\tmp\api_audio\lyric_test.mp3"
	)
	print(result["transcript"])