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
- `src/InstagramCommentTemplate.tsx`: layout do card de comentário.
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

Campos derivados na normalização:

- `username`: `author.username`, depois `username`, depois `UsuarioN`;
- `avatarUrl`: `author.profilePicUrl`, depois `profilePicUrl` ou `avatarUrl`;
- `commentText`: `text` ou `commentText`;
- `likes`: convertido para número, com padrão `0`;
- `time`: calculado a partir de `createdAtISO`/`createdAt`, ou usa `time`/`agora`;
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

O MCP usa `faster-whisper`. Quando existir um JSON em `timestamps/`, ele tenta alinhamento forçado com WhisperX; nesse caso, o pacote `whisperx` precisa estar instalado.

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

Use a ferramenta MCP `transcribe_audio(file_path)` quando for necessário copiar o áudio para `public/audio/`, atualizar `comments/comments.json` e obter timestamps.

Comportamento da ferramenta:

- valida o arquivo de áudio;
- copia o arquivo para `public/audio/<nome>`;
- define `audioPath` como `audio/<nome>`;
- usa o último JSON de comentários como fonte;
- salva o objeto consolidado em `comments/comments.json`;
- se houver timestamps externos, executa alinhamento forçado;
- caso contrário, transcreve em português com timestamps por palavra.

O JSON externo de timestamps pode conter `segments`, `phrases`, `lines`, `text` ou `transcript`. Para alinhamento por frases, mantenha o texto em português e as frases na ordem do áudio.

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
- Falha de alinhamento: compare as frases do JSON externo com o áudio e instale WhisperX.
- Bundle falha: execute `npm run lint` e corrija TypeScript/ESLint antes do render.
- Conteúdo do fundo não aparece: confirme o nome em `backgroundVideos` e a presença do arquivo em `public/`.

## Saída esperada

Entregue:

1. JSON de comentários consolidado;
2. áudio em `public/audio/`, quando aplicável;
3. composição Remotion atualizada e validada;
4. preview no Studio ou arquivo MP4 quando solicitado;
5. resumo dos arquivos alterados e do comando de validação executado.
