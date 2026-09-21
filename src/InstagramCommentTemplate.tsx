import React from 'react';
import { AbsoluteFill } from 'remotion';

// Definimos a interface de propriedades para que você possa injetar via automação
export type InstagramCommentProps = {
  username: string;
  avatarUrl: string;
  commentText: string;
  likes: number | string;
  time: string;
};

export const InstagramCommentTemplate: React.FC<InstagramCommentProps> = ({
  username,
  avatarUrl,
  commentText,
  likes,
  time,
}) => {
  return (
      <AbsoluteFill 
        style={{ 
          justifyContent: 'center', 
          alignItems: 'center', 
          padding: 40,
          fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif' 
        }}
      >
        {/* Caixa do Comentário (Estilo Card translúcido ou branco) */}
        <div style={{
          display: 'flex',
          flexDirection: 'row',
          backgroundColor: 'rgba(255, 255, 255, 0.96)', 
          padding: '35px',
          width: '100%',
          maxWidth: 900,
          boxShadow: '0 12px 40px rgba(0,0,0,0.3)',
          zIndex: 1,
        }}>
          
          {/* Foto de Perfil */}
          <div
            aria-label={avatarUrl}
            style={{
              width: 90, 
              height: 90, 
              borderRadius: '50%', 
              marginRight: 24,
              backgroundColor: '#e1e1e1',
              color: '#4a4a4a',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 34,
              fontWeight: 700,
            }}
          >
            {username.slice(0, 1).toUpperCase()}
          </div>

          {/* Conteúdo Central do Comentário */}
          <div style={{ display: 'flex', flexDirection: 'column', flex: 1, justifyContent: 'center' }}>
            {/* Linha do Usuário e Tempo */}
            <div style={{ display: 'flex', alignItems: 'center', marginBottom: 8 }}>
              <span style={{ fontWeight: 600, fontSize: 28, color: '#000', marginRight: 12 }}>
                {username}
              </span>
              <span style={{ fontSize: 24, color: '#737373' }}>
                {time}
              </span>
            </div>
            
            {/* Texto do Comentário */}
            <span style={{ fontSize: 28, color: '#000', lineHeight: '1.4', marginBottom: 16 }}>
              {commentText}
            </span>
            
            {/* Botão de Responder */}
            <span style={{ fontSize: 24, color: '#737373', fontWeight: 600 }}>
              Responder
            </span>
          </div>

          {/* Seção do Like (Coração + Contagem) */}
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginLeft: 20, marginTop: 10 }}>
            <svg 
              width="32" height="32" viewBox="0 0 24 24" 
              fill="none" stroke="#737373" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"
            >
              <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path>
            </svg>
            <span style={{ fontSize: 22, color: '#737373', marginTop: 12, fontWeight: 500 }}>
              {likes}
            </span>
          </div>

        </div>
      </AbsoluteFill>
  );
};