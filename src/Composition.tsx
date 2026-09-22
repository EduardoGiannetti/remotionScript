import { Composition, random, staticFile } from "remotion";
import { LyricVideo, type LyricVideoProps } from "./lyricvideo";

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
};

const formatInstagramDate = (comment: RawComment) => {
  const dateValue = comment.createdAtISO
    ? new Date(comment.createdAtISO)
    : typeof comment.createdAt === "number"
      ? new Date(comment.createdAt * 1000)
      : null;

  if (!dateValue || Number.isNaN(dateValue.getTime())) {
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

const normalizeComment = (comment: RawComment, index: number) => {
  const username = comment.author?.username ?? comment.username ?? `Usuario${index + 1}`;
  const avatarUrl = comment.author?.profilePicUrl ?? comment.profilePicUrl ?? comment.avatarUrl ?? "";
  const commentText = comment.text ?? comment.commentText ?? "";
  const time = formatInstagramDate(comment);
  const startFrame = typeof comment.startFrame === "number" ? comment.startFrame : index * 90;
  const durationInFrames =
    typeof comment.durationInFrames === "number" ? comment.durationInFrames : 90;

  return {
    ...comment,
    username,
    avatarUrl,
    commentText,
    likes: Number(comment.likes ?? 0),
    time,
    startFrame,
    durationInFrames,
  };
};

const backgroundVideos = [
  "gtaramp.webm",
  "gtaramp2.webm",
  "minecraftparkour.webm",
  "minecraftparkour2.webm",
  "minecraftparkour3.webm",
  "subwaysurfers.webm",
];

const backgroundVideoSeed = `background-video-${Date.now()}`;
const selectedVideo =
  backgroundVideos[Math.floor(random(backgroundVideoSeed) * backgroundVideos.length)];

type CommentsFile = RawComment[] | { comments?: RawComment[]; audioPath?: string };

const commentFiles = require.context("../comments", false, /\.json$/i);
const latestCommentFile = commentFiles
  .keys()
  .sort((left, right) => (left < right ? -1 : left > right ? 1 : 0))
  .slice(-1)[0];

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

export const MyComposition: React.FC = () => {
  return (
    <Composition<any, LyricVideoProps>
      id="InstagramCommentVideo"
      component={LyricVideo}
      durationInFrames={totalDuration || 300}
      fps={30}
      width={1080}
      height={1920}
      defaultProps={{
        audioPath: "vaporwave.mp3",//!Array.isArray(commentsFile) ? commentsFile.audioPath ?? "" : "",
        bgVideoUrl: staticFile(selectedVideo),
        comments: normalizedComments,
      }}
    />
  );
};