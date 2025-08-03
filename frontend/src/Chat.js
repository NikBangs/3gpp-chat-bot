import React, { useState, useEffect, useRef } from "react";
import { marked } from "marked";

function Chat({ messages, onSend }) {
  const [input, setInput] = useState("");
  const bottomRef = useRef(null);

  const handleSubmit = (e) => {
    e.preventDefault();
    if (!input.trim()) return;
    onSend(input.trim());
    setInput("");
  };

  // Auto-scroll to latest message
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  return (
    <div className="chat-wrapper">
      <div className="chat-box">
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`chat-message ${msg.sender === "user" ? "user" : "assistant"}`}
          >
            <div
              className="chat-bubble"
              dangerouslySetInnerHTML={{
                __html:
                  msg.sender === "assistant"
                    ? marked.parse(msg.text)
                    : msg.text,
              }}
            />
          </div>
        ))}
        <div ref={bottomRef} />
      </div>

      <form onSubmit={handleSubmit} className="chat-input">
        <input
          type="text"
          placeholder="Ask a question..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
        />
        <button type="submit">Send</button>
      </form>
    </div>
  );
}

export default Chat;
