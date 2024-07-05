'use client';

import React, { useState, useEffect, useRef } from 'react';
import { Card, Text, ScrollArea, Button, Flex, Box, Container } from '@radix-ui/themes';
import ErrorChatBubble from './ErrorChatBubble';
import RecommendationChatBubble from './RecommendationChatBubble';
import FeedbackChatBubble from './FeedbackChatBubble';
import StatusUpdateChatBubble from "@/components/StatusUpdateChatBubble";

type MessageType = 'error_report' | 'chat' | 'system' | 'feedback';

interface Message {
  type: MessageType;
  content: string;
}

const ErrorMonitoringChat: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [websocket, setWebsocket] = useState<WebSocket | null>(null);
  const [feedbackText, setFeedbackText] = useState('');
  const [isFeedbackMode, setIsFeedbackMode] = useState(false);
  const scrollAreaRef = useRef<HTMLDivElement>(null);

useEffect(() => {
  console.log("Attempting to connect to WebSocket");
  const ws = new WebSocket('ws://localhost:8000/ws');
  setWebsocket(ws);

  ws.onopen = (event) => {
    console.log("WebSocket connection established");
  };

  ws.onmessage = (event) => {
    console.log("Received message:", event.data);
    const data = JSON.parse(event.data);
    setMessages((prevMessages) => [...prevMessages, data]);
  };

  ws.onerror = (error) => {
    console.error("WebSocket error:", error);
  };

  ws.onclose = (event) => {
    console.log("WebSocket connection closed:", event);
  };

  return () => {
    ws.close();
  };
}, []);

  useEffect(() => {
    if (scrollAreaRef.current) {
      scrollAreaRef.current.scrollTop = scrollAreaRef.current.scrollHeight;
    }
  }, [messages]);

  const sendMessage = (type: string, content: string) => {
    if (websocket) {
      websocket.send(JSON.stringify({ type, content }));
    }
  };

  const handleAccept = () => sendMessage('accept', "");
  const handleIgnore = () => sendMessage('ignore', "");

  const handleFeedback = () => {
    setIsFeedbackMode(true);
    setFeedbackText('');
  };

  const submitFeedback = () => {
    if (feedbackText.trim()) {
      sendMessage('feedback', feedbackText);
      setMessages((prevMessages) => [...prevMessages, { type: 'feedback', content: feedbackText }]);
      setFeedbackText('');
      setIsFeedbackMode(false);
    }
  };

  const cancelFeedback = () => {
    setIsFeedbackMode(false);
    setFeedbackText('');
  };

  return (
    <Container style={{ 
      display: 'flex', 
      justifyContent: 'center', 
      alignItems: 'center', 
      height: '100vh', 
      width: '100vw',
      background: 'var(--gray-2)',
    }}>
      <Card style={{ 
        width: '1200px', 
        height: '700px', 
        overflow: 'hidden',
        boxShadow: '0 10px 25px rgba(0,0,0,0.1)',
        border: 'none',
      }}>
        <Flex direction="column" style={{ height: '100%' }}>
          <Box p="4" style={{ 
            background: 'linear-gradient(45deg, var(--indigo-9), var(--violet-9))', 
            color: 'white' 
          }}>
            <Text size="5" weight="bold">Error Monitoring Chat</Text>
          </Box>
          <ScrollArea 
            style={{ 
              flex: 1, 
              padding: '16px',
              background: `url("data:image/svg+xml,%3Csvg width='20' height='20' viewBox='0 0 20 20' xmlns='http://www.w3.org/2000/svg'%3E%3Cg fill='%239C92AC' fill-opacity='0.05' fill-rule='evenodd'%3E%3Ccircle cx='3' cy='3' r='3'/%3E%3Ccircle cx='13' cy='13' r='3'/%3E%3C/g%3E%3C/svg%3E")`,
            }} 
            ref={scrollAreaRef}
          >
            <Flex direction="column" gap="3">
              {messages.map((message, index) => {
                switch (message.type) {
                  case 'error_report':
                    return <ErrorChatBubble key={index} content={message.content} />;
                  case 'chat':
                    return (
                      <RecommendationChatBubble
                        key={index}
                        content={message.content}
                        onAccept={handleAccept}
                        onFeedback={handleFeedback}
                        onIgnore={handleIgnore}
                      />
                    );
                  case 'feedback':
                    return <FeedbackChatBubble key={index} content={message.content} />;
                  default:
                    return <StatusUpdateChatBubble key={index} content={message.content}/>;
                }
              })}
            </Flex>
          </ScrollArea>
          <Box p="3" style={{ backgroundColor: 'white', borderTop: '1px solid var(--gray-5)' }}>
            <Flex direction="column" gap="2">
              <input
                type="text"
                placeholder={isFeedbackMode ? "Type your feedback here..." : "Feedback disabled"}
                value={feedbackText}
                onChange={(e) => setFeedbackText(e.target.value)}
                disabled={!isFeedbackMode}
                style={{
                  padding: '12px',
                  borderRadius: '8px',
                  border: '2px solid var(--indigo-6)',
                  width: '100%',
                  backgroundColor: isFeedbackMode ? 'white' : 'var(--gray-3)',
                  color: isFeedbackMode ? 'var(--gray-12)' : 'var(--gray-8)',
                  cursor: isFeedbackMode ? 'text' : 'not-allowed',
                  transition: 'all 0.2s ease-in-out',
                  boxShadow: isFeedbackMode ? '0 2px 5px rgba(0,0,0,0.1)' : 'none',
                }}
              />
              {isFeedbackMode ? (
                <Flex gap="2">
                  <Button onClick={submitFeedback} style={{ 
                    background: 'linear-gradient(45deg, var(--indigo-9), var(--violet-9))',
                    color: 'white',
                    transition: 'all 0.2s ease-in-out',
                  }}>
                    Submit Feedback
                  </Button>
                  <Button onClick={cancelFeedback} variant="soft">Cancel</Button>
                </Flex>
              ) : (
                <Button disabled style={{ opacity: 0.5 }}>Submit Feedback</Button>
              )}
            </Flex>
          </Box>
        </Flex>
      </Card>
    </Container>
  );
};

export default ErrorMonitoringChat;