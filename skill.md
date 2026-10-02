---
name: remotion
description: Gerar o vídeo vertical de comentários cantados do projeto Downloads/remotion a partir de uma música, chamando a ferramenta MCP transcribe_audio, que sincroniza a letra com os comentários e renderiza o MP4.
version: 2.0.0
---

# Skill: geração de vídeos com Remotion

Use esta skill quando o usuário pedir para gerar ou renderizar o vídeo de comentários de uma música no projeto `C:\Users\EduardoGiannetti\Downloads\remotion`.

## Regras

1. **Não edite nada no projeto Remotion** (`src/`, `comments/`, `public/`, `remotion.config.ts`, `package.json`). O MCP grava tudo o que a composição precisa e faz o render.
2. **Não rode `npm`, `npx remotion` nem o Studio.** A única ação é chamar a ferramenta MCP.
3. Só `file_path` é obrigatório. Passe os outros parâmetros apenas quando o usuário os informar.
4. Nunca copie valores de `.env` para prompts, logs ou respostas.

## Ação

Chame a ferramenta `transcribe_audio` do servidor MCP `whisperx-lyrics` (registrado em `.mcp.json`):

| Parâmetro | Obrigatório | Padrão | Descrição |
| --- | --- | --- | --- |
| `file_path` | sim | — | Caminho do MP3 da música (absoluto, relativo ao projeto ou a `public/`). |
| `lyrics_path` | não | detectado | JSON da letra: caminho, nome em `timestamps/` ou task_id. Sem ele, usa a letra cujo task_id aparece no nome do áudio ou a que melhor corresponde ao que foi cantado. |
| `comments_path` | não | mais recente em `comments/` | JSON de comentários de origem (Instagram ou TikTok). |
| `fps` | não | `30` | FPS da composição. |
| `hold_seconds` | não | `1.5` | Tempo extra do comentário na tela após o fim da frase. |

Exemplo:

```json
{ "file_path": "C:\\Users\\EduardoGiannetti\\Downloads\\musica_5fc1552d_1.mp3" }
```

A execução leva alguns minutos (transcrição com WhisperX e render do Remotion). Aguarde o retorno sem executar outras ações no projeto.

## O que o MCP faz automaticamente

1. Transcreve a música e alinha cada frase da letra no tempo.
2. Associa cada frase cantada ao comentário de origem.
3. Copia o áudio para `public/audio/` e grava `comments/comments.json` (comentários com `startFrame`/`durationInFrames`, `audioPath` e `fps`), que a composição `InstagramCommentVideo` lê sozinha.
4. Grava o diagnóstico em `timestamps/aligned/<nome>.json`.
5. Renderiza o vídeo em `out/<nome-do-audio>.mp4`.

## Resposta ao usuário

Com base no retorno da ferramenta, informe:

- `videoPath`: caminho do MP4 gerado;
- quantas frases (`phrases`) entraram no vídeo e a duração (`durationSeconds`);
- `lyricsFile` e `commentsSource` usados;
- `skippedLyrics` (frases da letra que não foram cantadas) e `unmatchedPhrases` (frases sem comentário correspondente, que ficaram fora do vídeo), se houver.

## Falhas

Repasse a mensagem de erro da ferramenta ao usuário e sugira a correção. Não tente corrigir editando o projeto.

- `Arquivo de áudio não encontrado`: confirme o caminho do MP3.
- `Nenhuma letra (*_lyrics.json) encontrada` / `Letra não encontrada`: a letra precisa estar em `timestamps/`, ou informe `lyrics_path`.
- `Nenhum arquivo de comentários encontrado`: coloque o JSON de comentários em `comments/` ou informe `comments_path`.
- `Nenhuma frase ... foi associada a um comentário`: a letra ou os comentários não correspondem à música; confira `lyrics_path` e `comments_path`.
- `Falha ao renderizar o vídeo`: o render do Remotion falhou; informe o código de erro ao usuário.
- Ferramenta indisponível: o servidor `whisperx-lyrics` não está conectado; peça ao usuário para verificar o `.mcp.json` e o ambiente `.venv`.
