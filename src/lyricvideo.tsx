import React from 'react';
import { AbsoluteFill, Audio, Loop, Sequence, Video, staticFile, useCurrentFrame } from 'remotion';
import { InstagramCommentTemplate, type InstagramCommentProps } from './InstagramCommentTemplate';

export type LyricComment = InstagramCommentProps & {
  startFrame: number;
  durationInFrames: number;
};

export type LyricVideoProps = {
  bgVideoUrl: string;
  audioPath: string;
  comments: LyricComment[];
  introDurationInFrames: number;
};

export const LyricVideo: React.FC<LyricVideoProps> = ({
  bgVideoUrl,
  audioPath,
  comments,
  introDurationInFrames,
}) => {
  const frame = useCurrentFrame();
  const safeIntroDurationInFrames = Number.isFinite(introDurationInFrames)
    ? Math.max(1, Math.floor(introDurationInFrames))
    : 300;
  const commentsFrame = frame - safeIntroDurationInFrames;
  const audioSrc = /^(https?:|data:|blob:)/.test(audioPath)
    ? audioPath
    : staticFile(audioPath);
  const activeComment = comments.find(
    (comment) =>
      commentsFrame >= comment.startFrame &&
      commentsFrame < comment.startFrame + comment.durationInFrames,
  );

  return (
    <AbsoluteFill style={{ backgroundColor: '#000', zIndex: 0 }}>
      {/* O vídeo de fundo e o áudio tocam de forma contínua */}
      <Sequence from={0} durationInFrames={safeIntroDurationInFrames}>
        <Video
          src={bgVideoUrl}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      </Sequence>

      <Sequence from={safeIntroDurationInFrames}>
        <Loop durationInFrames={safeIntroDurationInFrames}>
          <Video
            src={bgVideoUrl}
            muted
            style={{
              width: '100%',
              height: '100%',
              objectFit: 'cover',
              filter: 'blur(7px)',
              transform: 'scale(1.02)',
            }}
          />
        </Loop>
        {audioPath && <Audio src={audioSrc} />}
      </Sequence>

      {activeComment ? <InstagramCommentTemplate {...activeComment} /> : null}
    </AbsoluteFill>
  );
};