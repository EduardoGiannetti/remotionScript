---
name: mmd
description: Gerar vídeos verticais de comentários usando o fluxo Remotion do projeto Downloads/remotion, com seleção de comentários, transcrição/alinhamento de áudio, composição React e renderização MP4.
version: 1.0.0
---

# Skill: geração de vídeos com Remotion

Use esta skill quando o usuário pedir para criar, atualizar, pré-visualizar ou renderizar um vídeo baseado no projeto:

`C:\Users\EduardoGiannetti\Downloads\remotion`

## Objetivo

Transformar comentários coletados em um vídeo vertical estilo short/reel:

- comentários normalizados e exibidos como cards;
- vídeo de fundo em formato vertical, com loop após a introdução;
- áudio local ou remoto sincronizado à composição;
- duração calculada a partir do vídeo de fundo e dos comentários;
- saída renderizada pelo Remotion.

## Regras de execução

1. Inspecione primeiro o projeto existente. Não faça scaffold se `package.json`, `src/Root.tsx` e `src/Composition.tsx` já estiverem presentes.
2. Preserve a estrutura atual e faça alterações pequenas, localizadas e compatíveis com React/TypeScript.
3. Antes de renderizar, execute `npm run lint`.
4. Para uma alteração visual, abra o Studio e valide a composição `InstagramCommentVideo`.
5. Só renderize um arquivo final quando isso for solicitado explicitamente.
6. Nunca copie valores de `.env` para prompts, documentação, gráficos, logs ou código. Use variáveis de ambiente e substitua segredos expostos por chaves novas.
7. Mantenha dados pessoais e URLs de avatar apenas quando forem necessários para o vídeo; não os replique em documentação de exemplo.

## Entradas e artefatos

Diretórios principais:

- `comments/`: JSON de comentários. O arquivo mais recente por ordem lexicográfica é carregado.
- `public/`: vídeos, áudios e outros arquivos estáticos usados por `staticFile()`.
- `timestamps/`: transcrições ou alinhamentos em JSON.
- `src/Composition.tsx`: registro da composição, normalização e metadados.
- `src/lyricvideo.tsx`: montagem do vídeo, áudio, loop e comentário ativo.
- `src/InstagramCommentTemplate.tsx`: layout do card de comentário do Instagram.
- `src/TikTokCommentTemplate.tsx`: layout do card de comentário do TikTok.
- `whisper_mcp_server.py`: ferramenta MCP `transcribe_audio`.
- `remotion.config.ts`: Rspack, JPEG e Tailwind v4.

Formato aceito para cada comentário:

```json
{
	"username": "usuario",
	"author": {
		"username": "usuario",
		"profilePicUrl": "https://..."
	},
	"profilePicUrl": "https://...",
	"avatarUrl": "https://...",
	"text": "Texto do comentário",
	"commentText": "Texto alternativo",
	"likes": 42,
	"time": "2h",
	"createdAtISO": "2026-09-23T12:00:00.000Z",
	"createdAt": 1780000000,
	"startFrame": 0,
	"durationInFrames": 90
}
```

O arquivo também pode ser um objeto:

```json
{
	"comments": [],
	"audioPath": "audio/minha-musica.mp3"
}
```

Comentários do TikTok são aceitos no formato do scraper:

```json
{
	"text": "Texto do comentário",
	"diggCount": 12,
	"createTimeISO": "2026-09-09T00:42:00.000Z",
	"uniqueId": "usuario",
	"avatarThumbnail": "https://...",
	"startFrame": 0,
	"durationInFrames": 90
}
```

Campos derivados na normalização:

- `platform`: usa `platform` (`instagram`/`tiktok`) se informado; senão vira `tiktok` quando existe `uniqueId`, `diggCount`, `avatarThumbnail` ou `createTimeISO`. Define o card usado: `src/InstagramCommentTemplate.tsx` ou `src/TikTokCommentTemplate.tsx`;
- `username`: `author.username`, depois `username`, depois `uniqueId`, depois `UsuarioN`;
- `avatarUrl`: `author.profilePicUrl`, depois `profilePicUrl`, `avatarUrl` ou `avatarThumbnail`;
- `commentText`: `text` ou `commentText`;
- `likes`: `likes` ou `diggCount`, convertido para número, com padrão `0` (o card do TikTok abrevia como `1.2K`);
- `time`: calculado a partir de `createdAtISO`/`createdAt` ou `createTimeISO`/`createTime`, ou usa `time`/`agora`. No TikTok, datas com mais de 7 dias aparecem como `DD-MM`;
- `startFrame`: usa o valor recebido ou `index * 90`;
- `durationInFrames`: usa o valor recebido ou `90`.

## Fluxo operacional

### 1. Preparar dependências

No diretório do projeto:

```powershell
cd C:\Users\EduardoGiannetti\Downloads\remotion
npm install
```

Dependências Python do MCP, quando a transcrição for necessária:

```powershell
python -m pip install -r requirements.txt
```

O MCP usa WhisperX (que traz o `faster-whisper`) e o SDK `mcp` 2.x. Os modelos `medium` e de alinhamento em português ficam no cache do Hugging Face após o primeiro uso.

### 2. Preparar comentários

Coloque o JSON em `comments/`. Para um vídeo determinado, prefira um nome ordenável por data, por exemplo `comentarios-AAAAMMDD_HHMMSS.json`.

Se houver uma etapa de seleção, ela deve:

1. escolher o arquivo de comentários de origem;
2. validar que a raiz é uma lista ou um objeto com `comments`;
3. remover itens sem texto útil;
4. limitar a quantidade de comentários quando solicitado;
5. preservar `likes`, autoria e timestamps necessários para a composição;
6. escrever um JSON válido em `comments/`.

### 3. Preparar áudio e transcrição

Use a ferramenta MCP `transcribe_audio(file_path, lyrics_path?, comments_path?, fps=30, hold_seconds=1.5)` do servidor `whisperx-lyrics` (registrado em `.mcp.json`). Sem MCP, o mesmo fluxo roda com:

```powershell
.venv\Scripts\python.exe whisper_mcp_server.py <musica.mp3> [--lyrics <task_id ou arquivo>]
```

Comportamento da ferramenta:

- transcreve a música com WhisperX (modelo `medium`, CPU) e alinha cada palavra no tempo;
- usa a letra `timestamps/<task_id>_lyrics.json` (campo `text`, ignorando marcações como `[Chorus]`). Sem `lyrics_path`, escolhe a letra cujo task_id aparece no nome do áudio ou, na falta dele, a que melhor corresponde ao que foi cantado;
- localiza cada frase da letra na transcrição aceitando repetições, frases puladas e fora de ordem (a música de IA não segue a letra à risca) e realinha o texto exato da letra para refinar os tempos;
- associa cada frase cantada ao comentário de origem (o JSON mais recente em `comments/`), tolerando emojis e acentos removidos na letra;
- grava `comments/comments.json` com um item por frase cantada: todos os campos do comentário + `startFrame` e `durationInFrames`. Frase repetida gera um item por repetição;
- `durationInFrames` vai do início da frase até `hold_seconds` após o fim dela, limitado pelo início da frase seguinte;
- copia o áudio para `public/audio/<nome>` e define `audioPath` como `audio/<nome>`;
- grava o diagnóstico (transcrição, palavras, tempos do ASR e refinados, frases puladas) em `timestamps/aligned/<nome>.json`.

A execução leva cerca de 1 a 2 minutos para uma música de 90 s. Confira no retorno `skippedLyrics` (frases que a IA não cantou) e `unmatchedPhrases` (frases sem comentário correspondente, que ficam fora do vídeo).

### 4. Verificar composição

Antes do Studio, confirme:

- ID: `InstagramCommentVideo`;
- dimensão: `1080x1920`;
- FPS: `30`;
- vídeo de fundo disponível em `public/`;
- áudio resolvível por `staticFile()` ou URL `http`, `https`, `data` ou `blob`;
- pelo menos um JSON válido em `comments/`.

O `Composition.tsx` calcula:

`duração = duração_do_vídeo_de_fundo + max(300, maior_startFrame + durationInFrames)`

O vídeo de fundo é reproduzido sem áudio na parte dos comentários, com blur de `7px` e escala `1.02`. O áudio começa após a introdução. O comentário ativo é o único cujo intervalo contém o frame atual.

### 5. Pré-visualizar e validar

```powershell
npm run lint
npx remotion studio --no-open
```

No Studio, valide a composição `InstagramCommentVideo`, a introdução, a transição para comentários, o loop do fundo, a sincronização do áudio, a leitura dos cards e o último comentário.

### 6. Renderizar

Render padrão:

```powershell
npx remotion render
```

Render explícito da composição:

```powershell
npx remotion render src/index.ts InstagramCommentVideo out/video.mp4
```

Para uma imagem estática:

```powershell
npx remotion still src/index.ts InstagramCommentVideo out/frame.png
```

## Checklist de falhas

- `Nenhum arquivo JSON encontrado`: coloque um JSON válido em `comments/`.
- Áudio não encontrado: copie-o para `public/audio/` ou use uma URL suportada.
- Duração incorreta: valide `startFrame`, `durationInFrames` e a duração real do vídeo.
- Card vazio: confirme `text`/`commentText` e os fallbacks de autoria.
- Frase faltando ou no lugar errado: veja `timestamps/aligned/<nome>.json` (transcrição do ASR, similaridade de cada frase, `skippedLyrics`) e confirme se a letra usada é a da música.
- Bundle falha: execute `npm run lint` e corrija TypeScript/ESLint antes do render.
- Conteúdo do fundo não aparece: confirme o nome em `backgroundVideos` e a presença do arquivo em `public/`.

## Saída esperada

Entregue:

1. JSON de comentários consolidado;
2. áudio em `public/audio/`, quando aplicável;
3. composição Remotion atualizada e validada;
4. preview no Studio ou arquivo MP4 quando solicitado;
5. resumo dos arquivos alterados e do comando de validação executado.
