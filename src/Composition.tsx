import { Composition, random, staticFile } from "remotion";
import { getVideoMetadata } from "@remotion/media-utils";
import { LyricVideo, type CommentPlatform } from "./lyricvideo";

declare const require: {
  context: (
    directory: string,
    useSubdirectories: boolean,
    pattern: RegExp,
  ) => {
    keys: () => string[];
    <T>(fileName: string): T;
  };
};

// O bundler do Remotion injeta as variáveis de ambiente com prefixo REMOTION_.
declare const process: { env: Record<string, string | undefined> };

type RawComment = {
  username?: string;
  author?: {
    username?: string;
    profilePicUrl?: string;
  };
  profilePicUrl?: string;
  avatarUrl?: string;
  text?: string;
  commentText?: string;
  likes?: number | string;
  time?: string;
  createdAtISO?: string;
  createdAt?: number;
  startFrame?: number;
  durationInFrames?: number;
  platform?: CommentPlatform;
  // Campos do JSON do TikTok
  uniqueId?: string;
  avatarThumbnail?: string;
  diggCount?: number | string;
  createTimeISO?: string;
  createTime?: number;
};

// Os campos exclusivos do scraper do TikTok identificam a origem do comentário.
const detectPlatform = (comment: RawComment): CommentPlatform => {
  if (comment.platform) return comment.platform;
  const isTikTok =
    comment.uniqueId !== undefined ||
    comment.diggCount !== undefined ||
    comment.avatarThumbnail !== undefined ||
    comment.createTimeISO !== undefined;
  return isTikTok ? "tiktok" : "instagram";
};

const parseCommentDate = (comment: RawComment) => {
  const isoDate = comment.createdAtISO ?? comment.createTimeISO;
  const unixSeconds = comment.createdAt ?? comment.createTime;
  const dateValue = isoDate
    ? new Date(isoDate)
    : typeof unixSeconds === "number"
      ? new Date(unixSeconds * 1000)
      : null;

  return dateValue && !Number.isNaN(dateValue.getTime()) ? dateValue : null;
};

const formatInstagramDate = (comment: RawComment) => {
  const dateValue = parseCommentDate(comment);

  if (!dateValue) {
    return comment.time ?? "agora";
  }

  const elapsedMinutes = Math.max(0, Math.floor((Date.now() - dateValue.getTime()) / 60000));
  const elapsedHours = Math.floor(elapsedMinutes / 60);
  const elapsedDays = Math.floor(elapsedHours / 24);
  const elapsedWeeks = Math.floor(elapsedDays / 7);

  if (elapsedMinutes < 60) return `${elapsedMinutes}m`;
  if (elapsedHours < 24) return `${elapsedHours}h`;
  if (elapsedDays < 7) return `${elapsedDays}d`;

  return `${elapsedWeeks} sem`;
};

// O TikTok usa tempo relativo na primeira semana e depois a data como MM-DD.
const formatTikTokDate = (comment: RawComment) => {
  const dateValue = parseCommentDate(comment);

  if (!dateValue) {
    return comment.time ?? "agora";
  }

  const elapsedMinutes = Math.max(0, Math.floor((Date.now() - dateValue.getTime()) / 60000));
  const elapsedHours = Math.floor(elapsedMinutes / 60);
  const elapsedDays = Math.floor(elapsedHours / 24);

  if (elapsedMinutes < 1) return "agora";
  if (elapsedMinutes < 60) return `${elapsedMinutes}min`;
  if (elapsedHours < 24) return `${elapsedHours}h`;
  if (elapsedDays < 7) return `${elapsedDays}d`;

  const day = `0${dateValue.getDate()}`.slice(-2);
  const month = `0${dateValue.getMonth() + 1}`.slice(-2);
  return `${month}-${day}`;
};

const normalizeComment = (comment: RawComment, index: number) => {
  const platform = detectPlatform(comment);
  const username =
    comment.author?.username ?? comment.username ?? comment.uniqueId ?? `Usuario${index + 1}`;
  const avatarUrl =
    comment.author?.profilePicUrl ??
    comment.profilePicUrl ??
    comment.avatarUrl ??
    comment.avatarThumbnail ??
    "";
  const commentText = comment.text ?? comment.commentText ?? "";
  const time = platform === "tiktok" ? formatTikTokDate(comment) : formatInstagramDate(comment);
  const startFrame = typeof comment.startFrame === "number" ? comment.startFrame : index * 90;
  const durationInFrames =
    typeof comment.durationInFrames === "number" ? comment.durationInFrames : 90;

  return {
    ...comment,
    platform,
    username,
    avatarUrl,
    commentText,
    likes: Number(comment.likes ?? comment.diggCount ?? 0),
    time,
    startFrame,
    durationInFrames,
  };
};

// Vídeo original: toca inteiro na abertura e pode virar o fundo dos comentários.
const originalVideo = "cuida.mp4";

// Templates que podem substituir o vídeo original como fundo dos comentários.
const templateVideos = [
  "danca.mp4",
];

const templateVideoSeed = `template-video-${Date.now()}`;
const selectedTemplate =
  templateVideos[Math.floor(random(templateVideoSeed) * templateVideos.length)];

// Escolha do fundo depois do vídeo original. Também podem ser trocados no render com
// --props='{"useTemplateBackground":true}' ou --props='{"loopBackground":false}',
// ou pelas variáveis REMOTION_USE_TEMPLATE_BACKGROUND e REMOTION_LOOP_BACKGROUND
// ("true"/"false"), que o whisper_mcp_server.py define ao renderizar.
const parseBooleanEnv = (value: string | undefined, fallback: boolean) =>
  value === undefined || value === "" ? fallback : value.toLowerCase() === "true";

const defaultUseTemplateBackground = parseBooleanEnv(
  process.env.REMOTION_USE_TEMPLATE_BACKGROUND,
  true,
);
const defaultLoopBackground = parseBooleanEnv(process.env.REMOTION_LOOP_BACKGROUND, true);

type CommentsFile =
  | RawComment[]
  | { comments?: RawComment[]; audioPath?: string; fps?: number };

const commentFiles = require.context("../comments", false, /\.json$/i);
const commentFileNames = commentFiles
  .keys()
  .sort((left, right) => (left < right ? -1 : left > right ? 1 : 0));
// comments.json é gerado pelo whisper_mcp_server.py com o tempo de cada frase;
// sem ele, usa o arquivo de comentários mais recente.
const latestCommentFile =
  commentFileNames.find((fileName) => fileName.endsWith("/comments.json")) ??
  commentFileNames.slice(-1)[0];

if (!latestCommentFile) {
  throw new Error("Nenhum arquivo JSON encontrado na pasta comments");
}

const commentsFile = commentFiles<CommentsFile>(latestCommentFile);
const rawComments = Array.isArray(commentsFile)
  ? commentsFile
  : commentsFile.comments ?? [];

const normalizedComments = rawComments.map(normalizeComment);

const totalDuration = normalizedComments.reduce(
  (latestEndFrame, item) => Math.max(latestEndFrame, item.startFrame + item.durationInFrames),
  0,
);

const defaultIntroDurationInFrames = 300;
// Os startFrame/durationInFrames do JSON foram calculados com este FPS.
const fps = (!Array.isArray(commentsFile) && commentsFile.fps) || 30;

const calculateVideoDurationInFrames = async (src: string) => {
  const metadata = await getVideoMetadata(src);
  return Math.max(1, Math.ceil(metadata.durationInSeconds * fps));
};

// Os últimos frames costumam ser fade para preto, então congela ~1s antes do fim.
// Em vídeos com menos de 2s, usa o meio do vídeo.
const calculateStillFrame = (videoDurationInFrames: number) =>
  videoDurationInFrames > 2 * fps
    ? videoDurationInFrames - fps
    : Math.floor(videoDurationInFrames / 2);

export const MyComposition: React.FC = () => {
  return (
    <Composition
      id="InstagramCommentVideo"
      component={LyricVideo}
      durationInFrames={defaultIntroDurationInFrames + (totalDuration || 300)}
      fps={fps}
      width={1080}
      height={1920}
      calculateMetadata={async ({props}) => {
        const backgroundVideoDurationInFrames = await calculateVideoDurationInFrames(
          props.bgVideoUrl,
        );
        const introDurationInFrames = backgroundVideoDurationInFrames;
        const durationInFrames = introDurationInFrames + (totalDuration || 300);
        // O template só existe com loop: template + imagem estática não é uma saída válida.
        const useTemplateBackground = props.useTemplateBackground && Boolean(props.templateVideoUrl);
        const loopBackground = useTemplateBackground || props.loopBackground;
        const templateVideoDurationInFrames = useTemplateBackground
          ? await calculateVideoDurationInFrames(props.templateVideoUrl)
          : props.templateVideoDurationInFrames;

        return {
          durationInFrames,
          props: {
            ...props,
            introDurationInFrames,
            backgroundVideoDurationInFrames,
            durationInFrames,
            useTemplateBackground,
            loopBackground,
            templateVideoDurationInFrames,
            stillFrame: props.stillFrame ?? calculateStillFrame(backgroundVideoDurationInFrames),
          },
        };
      }}
      defaultProps={{
        audioPath: !Array.isArray(commentsFile)
          ? commentsFile.audioPath ?? "vaporwave.mp3"
          : "vaporwave.mp3",
        bgVideoUrl: staticFile(originalVideo),
        comments: normalizedComments,
        introDurationInFrames: defaultIntroDurationInFrames,
        backgroundVideoDurationInFrames: defaultIntroDurationInFrames,
        durationInFrames: defaultIntroDurationInFrames + (totalDuration || 300),
        useTemplateBackground: defaultUseTemplateBackground,
        loopBackground: defaultLoopBackground,
        templateVideoUrl: staticFile(selectedTemplate),
        templateVideoDurationInFrames: defaultIntroDurationInFrames,
      }}
    />
  );
};