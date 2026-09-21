import React from 'react';
import { AbsoluteFill, Audio, Video, staticFile, useCurrentFrame } from 'remotion';
import { InstagramCommentTemplate, type InstagramCommentProps } from './InstagramCommentTemplate';

export type LyricComment = InstagramCommentProps & {
  startFrame: number;
  durationInFrames: number;
};

export type LyricVideoProps = {
  bgVideoUrl: string;
  audioPath: string;
  comments: LyricComment[];
};

export const LyricVideo: React.FC<LyricVideoProps> = ({ bgVideoUrl, audioPath, comments }) => {
  const frame = useCurrentFrame();
  const audioSrc = /^(https?:|data:|blob:)/.test(audioPath)
    ? audioPath
    : staticFile(audioPath);
  const activeComment = comments.find(
    (comment) =>
      frame >= comment.startFrame &&
      frame < comment.startFrame + comment.durationInFrames,
  );

  return (
    <AbsoluteFill style={{ backgroundColor: '#000', zIndex: 0 }}>
      {/* O vídeo de fundo e o áudio tocam de forma contínua */}
      <Video src={bgVideoUrl} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      {audioPath && <Audio src={audioSrc} />}

      {activeComment ? <InstagramCommentTemplate {...activeComment} /> : null}
    </AbsoluteFill>
  );
};