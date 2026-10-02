import React from 'react';
import { AbsoluteFill } from 'remotion';
import { CommentAvatar } from './CommentAvatar';

// Mesmas propriedades do card do Instagram, para o LyricVideo trocar de template sem conversão
export type TikTokCommentProps = {
  username: string;
  avatarUrl: string;
  commentText: string;
  likes: number | string;
  time: string;
};

// O TikTok abrevia contagens grandes: 1234 -> 1.2K, 1500000 -> 1.5M
const formatTikTokCount = (likes: number | string) => {
  const value = Number(likes);
  if (!Number.isFinite(value)) return String(likes);
  if (value >= 1_000_000) return `${(value / 1_000_000).toFixed(1).replace(/\.0$/, '')}M`;
  if (value >= 1_000) return `${(value / 1_000).toFixed(1).replace(/\.0$/, '')}K`;
  return String(value);
};

export const TikTokCommentTemplate: React.FC<TikTokCommentProps> = ({
  username,
  avatarUrl,
  commentText,
  likes,
  time,
}) => {
  const shortUsername = username || 'Usuário';
  const avatar = avatarUrl || 'https://github.com/github.png';

  return (
      <AbsoluteFill
        style={{
          justifyContent: 'center',
          alignItems: 'center',
          padding: 40,
          fontFamily: '"TikTok Sans", "Proxima Nova", -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif'
        }}
      >
        {/* Caixa do Comentário (folha de comentários branca do TikTok) */}
        <div style={{
          display: 'flex',
          flexDirection: 'row',
          backgroundColor: 'rgba(255, 255, 255, 1)',
          padding: '35px',
          width: '100%',
          maxWidth: 900,
          borderRadius: 24,
          boxShadow: '0 12px 40px rgba(0,0,0,0.3)',
          zIndex: 1,
        }}>

          {/* Foto de Perfil */}
          <CommentAvatar
            src={avatar}
            username={shortUsername}
            style={{ width: 90, height: 90, flexShrink: 0, marginRight: 24 }}
          />

          {/* Conteúdo Central do Comentário */}
          <div style={{ display: 'flex', flexDirection: 'column', flex: 1, justifyContent: 'center' }}>
            {/* No TikTok o nome fica acima do texto, em cinza */}
            <span style={{ fontWeight: 600, fontSize: 26, color: '#8a8b91', marginBottom: 8 }}>
              {shortUsername}
            </span>

            {/* Texto do Comentário */}
            <span style={{ fontSize: 30, color: '#161823', lineHeight: '1.4', marginBottom: 14, whiteSpace: 'pre-line' }}>
              {commentText}
            </span>

            {/* Linha de ações: Data e Responder à esquerda; Like, contagem e Dislike à direita */}
            <div style={{ display: 'flex', alignItems: 'center' }}>
              <span style={{ fontSize: 24, color: '#8a8b91', marginRight: 28 }}>
                {time}
              </span>
              <span style={{ fontSize: 24, color: '#8a8b91', fontWeight: 600 }}>
                Responder
              </span>

              <div style={{ display: 'flex', alignItems: 'center', marginLeft: 'auto' }}>
                <svg
                  width="30" height="30" viewBox="0 0 24 24"
                  fill="none" stroke="#8a8b91" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
                >
                  <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
                </svg>
                <span style={{ fontSize: 22, color: '#8a8b91', marginLeft: 8, marginRight: 28, fontWeight: 500 }}>
                  {formatTikTokCount(likes)}
                </span>
                <svg
                  width="30" height="30" viewBox="0 0 24 24"
                  fill="none" stroke="#8a8b91" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"
                >
                  <path d="M10 15v4a3 3 0 0 0 3 3l4-9V2H5.72a2 2 0 0 0-2 1.7l-1.38 9a2 2 0 0 0 2 2.3zm7-13h2.67A2.31 2.31 0 0 1 22 4v7a2.31 2.31 0 0 1-2.33 2H17"></path>
                </svg>
              </div>
            </div>
          </div>

        </div>
      </AbsoluteFill>
  );
};
