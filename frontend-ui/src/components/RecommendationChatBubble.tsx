import React from 'react';
import { Card, Text, Button, Flex, Box } from '@radix-ui/themes';
import ReactMarkdown from 'react-markdown';

interface RecommendationChatBubbleProps {
  content: string; // This is Markdown content
  onAccept: () => void;
  onFeedback: () => void;
  onIgnore: () => void;
}

const RecommendationChatBubble: React.FC<RecommendationChatBubbleProps> = ({
  content,
  onAccept,
  onFeedback,
  onIgnore,
}) => {
  return (
    <Card
      style={{
        maxWidth: '80%',
        marginBottom: '10px',
        backgroundColor: 'var(--green-3)', // Light green background
        border: '1px solid var(--green-6)',
      }}
    >
      <Box p="3">
        <Text
          size="2"
          weight="bold"
          style={{ color: 'var(--green-11)', marginBottom: '4px' }}
        >
          Recommended Solution:
        </Text>
        {/* Wrap ReactMarkdown in a div to apply styles */}
        <div style={{ color: 'var(--green-11)', marginBottom: '8px' }}>
          <ReactMarkdown>{content}</ReactMarkdown>
        </div>
        <Flex gap="2" mt="2">
          <Button onClick={onAccept} variant="soft" color="green">Accept</Button>
          <Button onClick={onFeedback} variant="soft" color="blue">Feedback</Button>
          <Button onClick={onIgnore} variant="soft" color="gray">Ignore</Button>
        </Flex>
      </Box>
    </Card>
  );
};

export default RecommendationChatBubble;