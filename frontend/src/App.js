import { useState } from "react";
import Graph from "./Graph";
import Chat from "./Chat";

export default function App() {
  const [highlightedNodes, setHighlightedNodes] = useState([]);
  const [messages, setMessages] = useState([]);

  const handleUserQuery = async (query) => {
    setMessages((msgs) => [...msgs, { sender: "user", text: query }]);
    try {
      const response = await fetch("http://localhost:5000/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query }),
      });
  
      const data = await response.json();
  
      const botReply = data.answer || "Sorry, I couldn't find anything.";
      setMessages((msgs) => [...msgs, { sender: "bot", text: botReply }]);
  
      setHighlightedNodes(data.highlight || []);
    } catch (error) {
      console.error("Query failed", error);
      setMessages((msgs) => [
        ...msgs,
        { sender: "bot", text: "Server error. Please try again." },
      ]);
    }
  };

  return (
    <div style={{ display: "flex", height: "100vh", overflow: "hidden" }}>
      <div style={{ flex: 1, borderRight: "1px solid #ccc", overflow: "auto" }}>
        <Graph highlight={highlightedNodes} />
      </div>
      <div style={{ flex: 1.2, padding: "1rem", overflow: "auto" }}>
        <Chat messages={messages} onSend={handleUserQuery} />
      </div>
    </div>
  );
}