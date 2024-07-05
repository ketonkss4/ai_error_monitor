import React from 'react';
import { Card, Text, Box } from '@radix-ui/themes';
import ReactMarkdown from 'react-markdown';

interface FeedbackChatBubbleProps {
  content: string; // This is Markdown content
}

const FeedbackChatBubble: React.FC<FeedbackChatBubbleProps> = ({ content }) => {
  return (
    <Card
      style={{
        maxWidth: '80%',
        marginBottom: '10px',
        marginLeft: 'auto', // Align to the right
        backgroundColor: 'var(--gray-3)', // Light gray background
        border: '1px solid var(--gray-6)',
      }}
    >
      <Box p="3">
        <Text
          size="2"
          weight="bold"
          style={{ color: 'var(--gray-11)', marginBottom: '4px' }}
        >
          User Feedback:
        </Text>
        {/* Wrap ReactMarkdown in a div to apply styles */}
        <div style={{ color: 'var(--gray-12)' }}>
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
      </Box>
    </Card>
  );
};

export default FeedbackChatBubble;