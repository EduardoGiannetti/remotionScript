import { Composition, random, staticFile } from "remotion";
import { LyricVideo, type LyricVideoProps } from "./lyricvideo";
import mockData from "./comments.json";

const backgroundVideos = [
  "gtaramp.webm",
  "gtaramp2.webm",
  "minecraftparkour.webm",
  "minecraftparkour2.webm",
  "minecraftparkour3.webm",
  "subwaysurfers.webm",
];

const selectedVideo =
  backgroundVideos[Math.floor(random("background-video") * backgroundVideos.length)];

  const totalDuration = mockData.comments.reduce(
  (acc, item) => item.startFrame + item.durationInFrames,
  0
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
        audioPath: mockData.audioPath,
        bgVideoUrl: staticFile(selectedVideo),
        comments: mockData.comments,
      }}
    />
  );
};