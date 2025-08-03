import React, { useState, useEffect, useRef } from 'react';
import { marked } from 'marked';
import { Send } from 'lucide-react';

interface Message {
  id: string;
  sender: 'user' | 'assistant';
  text: string;
  timestamp: Date;
}

interface ChatPanelProps {
  messages: Message[];
  onSendMessage: (message: string) => void;
  isLoading?: boolean;
}

const ChatPanel: React.FC<ChatPanelProps> = ({ 
  messages, 
  onSendMessage, 
  isLoading = false 
}) => {
  const [inputValue, setInputValue] = useState('');
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  // Auto-scroll to bottom when new messages arrive
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Auto-resize textarea
  const adjustTextareaHeight = () => {
    const textarea = textareaRef.current;
    if (textarea) {
      textarea.style.height = '44px';
      textarea.style.height = Math.min(textarea.scrollHeight, 128) + 'px';
    }
  };

  useEffect(() => {
    adjustTextareaHeight();
  }, [inputValue]);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const trimmedInput = inputValue.trim();
    if (!trimmedInput || isLoading) return;
    
    onSendMessage(trimmedInput);
    setInputValue('');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit(e);
    }
  };

  const handleInputChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setInputValue(e.target.value);
  };

  const renderMessage = (message: Message) => {
    const isUser = message.sender === 'user';
    
    return (
      <div 
        key={message.id} 
        className={`message-container ${message.sender}`}
      >
        <div className={`message-bubble ${message.sender}`}>
          {isUser ? (
            <div>{message.text}</div>
          ) : (
            <div 
              className="message-content"
              dangerouslySetInnerHTML={{ 
                __html: marked.parse(message.text) 
              }} 
            />
          )}
        </div>
      </div>
    );
  };

  return (
    <div className="chat-panel">
      {/* Chat Header */}
      <div className="p-4 border-b border-chat-border">
        <h2 className="text-lg font-semibold">3GPP Assistant</h2>
        <p className="text-sm text-muted-foreground">
          Ask questions about 3GPP specifications and changes
        </p>
      </div>

      {/* Messages Area */}
      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="flex items-center justify-center h-full text-center">
            <div className="max-w-md">
              <h3 className="text-lg font-medium mb-2">Welcome to 3GPP Chat</h3>
              <p className="text-sm text-muted-foreground mb-4">
                I can help you understand 3GPP specifications, find specific information, 
                and explain changes between document versions.
              </p>
              <div className="text-xs text-muted-foreground space-y-1">
                <p>💡 Try asking: "What are the key changes in this version?"</p>
                <p>🔍 Or: "Explain the handover procedures"</p>
              </div>
            </div>
          </div>
        ) : (
          <>
            {messages.map(renderMessage)}
            {isLoading && (
              <div className="message-container assistant">
                <div className="message-bubble assistant">
                  <div className="flex items-center space-x-2">
                    <div className="flex space-x-1">
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce"></div>
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                      <div className="w-2 h-2 bg-current rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                    </div>
                    <span className="text-sm opacity-75">Thinking...</span>
                  </div>
                </div>
              </div>
            )}
          </>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="chat-input-area">
        <form onSubmit={handleSubmit} className="chat-input-container">
          <textarea
            ref={textareaRef}
            value={inputValue}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            placeholder="Ask about 3GPP specifications..."
            className="chat-input"
            rows={1}
            disabled={isLoading}
          />
          <button
            type="submit"
            disabled={!inputValue.trim() || isLoading}
            className="send-button"
            aria-label="Send message"
          >
            <Send size={16} />
          </button>
        </form>
        <div className="text-xs text-muted-foreground mt-2 px-1">
          Press Enter to send, Shift+Enter for new line
        </div>
      </div>
    </div>
  );
};

export default ChatPanel;