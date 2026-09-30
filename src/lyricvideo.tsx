import React from 'react';
import { AbsoluteFill, Audio, Loop, OffthreadVideo, Sequence, staticFile, useCurrentFrame } from 'remotion';
import { InstagramCommentTemplate, type InstagramCommentProps } from './InstagramCommentTemplate';
import { TikTokCommentTemplate } from './TikTokCommentTemplate';

export type CommentPlatform = 'instagram' | 'tiktok';

export type LyricComment = InstagramCommentProps & {
  platform?: CommentPlatform;
  startFrame: number;
  durationInFrames: number;
};

export type LyricVideoProps = {
  bgVideoUrl: string;
  audioPath: string;
  comments: LyricComment[];
  introDurationInFrames: number;
  backgroundVideoDurationInFrames: number;
  durationInFrames: number;
};

export const LyricVideo: React.FC<LyricVideoProps> = ({
  bgVideoUrl,
  audioPath,
  comments,
  introDurationInFrames,
  backgroundVideoDurationInFrames,
}) => {
  const frame = useCurrentFrame();
  const safeIntroDurationInFrames = Number.isFinite(introDurationInFrames)
    ? Math.max(1, Math.floor(introDurationInFrames))
    : 300;
  const commentsFrame = frame - safeIntroDurationInFrames;
  const safeBackgroundVideoDurationInFrames = Number.isFinite(backgroundVideoDurationInFrames)
    ? Math.max(1, Math.floor(backgroundVideoDurationInFrames))
    : 1;
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
      {/* O vídeo de fundo e o áudio tocam de forma contínua.
          OffthreadVideo extrai cada frame exato via FFmpeg no render; o <Video>
          HTML5 faz seek impreciso no Chrome e gera frames repetidos/fora de ordem. */}
      <Sequence durationInFrames={safeIntroDurationInFrames}>
        <OffthreadVideo
          src={bgVideoUrl}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      </Sequence>

      <Sequence from={safeIntroDurationInFrames}>
        <Loop durationInFrames={safeBackgroundVideoDurationInFrames}>
          <OffthreadVideo
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

      {activeComment?.platform === 'tiktok' ? (
        <TikTokCommentTemplate {...activeComment} />
      ) : activeComment ? (
        <InstagramCommentTemplate {...activeComment} />
      ) : null}
    </AbsoluteFill>
  );
};