import React from 'react';
import {
  AbsoluteFill,
  Audio,
  Freeze,
  Loop,
  OffthreadVideo,
  Sequence,
  staticFile,
  useCurrentFrame,
} from 'remotion';
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
  // Fundo depois do vídeo original. As combinações possíveis são:
  // original + loop, original + imagem estática e template + loop.
  useTemplateBackground: boolean;
  loopBackground: boolean;
  templateVideoUrl: string;
  templateVideoDurationInFrames: number;
  // Frame do vídeo original congelado quando loopBackground é false.
  stillFrame?: number;
};

const coverStyle: React.CSSProperties = {
  width: '100%',
  height: '100%',
  objectFit: 'cover',
};

const blurredCoverStyle: React.CSSProperties = {
  ...coverStyle,
  filter: 'blur(7px)',
  transform: 'scale(1.02)',
};

const toSafeFrameCount = (value: number | undefined, fallback: number) =>
  typeof value === 'number' && Number.isFinite(value) ? Math.max(1, Math.floor(value)) : fallback;

export const LyricVideo: React.FC<LyricVideoProps> = ({
  bgVideoUrl,
  audioPath,
  comments,
  introDurationInFrames,
  backgroundVideoDurationInFrames,
  useTemplateBackground,
  loopBackground,
  templateVideoUrl,
  templateVideoDurationInFrames,
  stillFrame,
}) => {
  const frame = useCurrentFrame();
  const safeIntroDurationInFrames = toSafeFrameCount(introDurationInFrames, 300);
  const commentsFrame = frame - safeIntroDurationInFrames;
  const safeBackgroundVideoDurationInFrames = toSafeFrameCount(backgroundVideoDurationInFrames, 1);
  const safeTemplateVideoDurationInFrames = toSafeFrameCount(templateVideoDurationInFrames, 1);
  const safeStillFrame = Math.min(
    safeBackgroundVideoDurationInFrames - 1,
    Math.max(0, Math.floor(stillFrame ?? safeBackgroundVideoDurationInFrames - 1)),
  );
  const showTemplate = useTemplateBackground && Boolean(templateVideoUrl);
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
        <OffthreadVideo src={bgVideoUrl} style={coverStyle} />
      </Sequence>

      <Sequence from={safeIntroDurationInFrames}>
        {showTemplate ? (
          // O template sempre fica em loop: não existe a opção template + imagem estática.
          <Loop durationInFrames={safeTemplateVideoDurationInFrames}>
            <OffthreadVideo src={templateVideoUrl} muted style={blurredCoverStyle} />
          </Loop>
        ) : loopBackground ? (
          <Loop durationInFrames={safeBackgroundVideoDurationInFrames}>
            <OffthreadVideo src={bgVideoUrl} muted style={blurredCoverStyle} />
          </Loop>
        ) : (
          <Freeze frame={safeStillFrame}>
            <OffthreadVideo src={bgVideoUrl} muted style={blurredCoverStyle} />
          </Freeze>
        )}
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