import React, { useState, useCallback } from 'react';
import GraphPanel from '../components/GraphPanel';
import ChatPanel from '../components/ChatPanel';

interface Message {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: Date;
}

const Index = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [highlightedNodes, setHighlightedNodes] = useState<string[]>([]);
  const [isLoading, setIsLoading] = useState(false);

  // Simulate API call to your backend
  const handleSendMessage = useCallback(async (messageText: string) => {
    const userMessage: Message = {
      id: Date.now().toString(),
      sender: 'user',
      text: messageText,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    setIsLoading(true);

    try {
      // Replace this with your actual API call
      const response = await fetch('http://localhost:5000/api/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: messageText }),
      });

      if (!response.ok) {
        throw new Error('Failed to get response');
      }

      const data = await response.json();

      const assistantMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: data.answer || 'I apologize, but I encountered an error processing your request.',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
      
      // Update highlighted nodes if provided
      if (data.highlight && Array.isArray(data.highlight)) {
        setHighlightedNodes(data.highlight);
      }

    } catch (error) {
      console.error('Error sending message:', error);
      
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        sender: 'assistant',
        text: '❌ Sorry, I encountered an error. Please make sure the backend server is running at http://localhost:5000',
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  }, []);

  return (
    <div className="app-layout">
      <GraphPanel 
        highlightedNodes={highlightedNodes}
        graphHtmlUrl="/data/graph.html"
      />
      <ChatPanel 
        messages={messages}
        onSendMessage={handleSendMessage}
        isLoading={isLoading}
      />
    </div>
  );
};

export default Index;
