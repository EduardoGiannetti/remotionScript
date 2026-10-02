import React, { useState } from 'react';
import { Img } from 'remotion';

type CommentAvatarProps = {
  src: string;
  username: string;
  style?: React.CSSProperties;
};

// <Img> faz o Remotion esperar a imagem carregar antes de capturar o frame, o que
// background-image não faz. Se a imagem falhar (ex.: URL expirada), mostra a inicial
// do usuário em vez de derrubar o render.
export const CommentAvatar: React.FC<CommentAvatarProps> = ({ src, username, style }) => {
  const [failed, setFailed] = useState(false);
  const showImage = Boolean(src) && !failed;

  return (
    <div
      style={{
        borderRadius: '50%',
        backgroundColor: '#e1e1e1',
        color: '#4a4a4a',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        fontSize: 34,
        fontWeight: 700,
        overflow: 'hidden',
        ...style,
      }}
    >
      {showImage ? (
        <Img
          src={src}
          onError={() => setFailed(true)}
          style={{ width: '100%', height: '100%', objectFit: 'cover' }}
        />
      ) : (
        username.slice(0, 1).toUpperCase()
      )}
    </div>
  );
};
