import React from 'react';
import { Card, Text, Box } from '@radix-ui/themes';
import ReactMarkdown from 'react-markdown';

interface StatusUpdateChatBubbleProps {
    content: string; // This is Markdown content
}

const StatusUpdateChatBubble: React.FC<StatusUpdateChatBubbleProps> = ({ content }) => {
    return (
        <Card
            style={{
                backgroundColor: '#e0e0e0', // Slightly darker grey for better contrast
                maxWidth: '80%',
                marginLeft: 'auto',
                marginRight: 'auto',
                marginBottom: '1rem',
            }}
        >
            <Box p="3">
                <Text weight="bold" mb="2" style={{ color: '#333333' }}>
                    System Status Update:
                </Text>
                <Box
                    style={{
                        backgroundColor: 'white',
                        padding: '0.5rem',
                        borderRadius: '4px',
                    }}
                >
                    <div style={{ color: '#1a1a1a' }}>
                        <ReactMarkdown>{content}</ReactMarkdown>
                    </div>
                </Box>
            </Box>
        </Card>
    );
};

export default StatusUpdateChatBubble;