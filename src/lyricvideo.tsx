import React from 'react';
import { AbsoluteFill, Video, Audio, Sequence, staticFile } from 'remotion';
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
  return (
    <AbsoluteFill style={{ backgroundColor: '#000' }}>
      {/* O vídeo de fundo e o áudio tocam de forma contínua */}
      <Video src={bgVideoUrl} muted style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
      {audioPath && <Audio src={staticFile(audioPath)} />}

      {/* Mapeia o JSON para criar uma sequência de entradas na tela */}
      {comments.map((comment, index) => (
        <Sequence 
          key={index} 
          from={comment.startFrame} 
          durationInFrames={comment.durationInFrames}
        >
          <InstagramCommentTemplate {...comment} />
        </Sequence>
      ))}
    </AbsoluteFill>
  );
};