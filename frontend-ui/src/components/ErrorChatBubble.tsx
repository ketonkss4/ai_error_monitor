import React from 'react';
import { Card, Box } from '@radix-ui/themes';
import ReactMarkdown from 'react-markdown';

interface ErrorChatBubbleProps {
  content: string; // This is Markdown content
}

const ErrorChatBubble: React.FC<ErrorChatBubbleProps> = ({ content }) => {
  return (
    <Card
      style={{
        maxWidth: '80%',
        marginBottom: '10px',
        backgroundColor: 'var(--red-3)', // Light red background
        border: '1px solid var(--red-6)',
      }}
    >
      <Box p="3" style={{ color: 'var(--red-11)', marginBottom: '4px', fontWeight: 'bold' }}>
        {/* Wrap ReactMarkdown in a div to apply styles */}
        <div style={{ color: 'inherit', marginBottom: 'inherit', fontWeight: 'inherit' }}>
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </Box>
    </Card>
  );
};

export default ErrorChatBubble;