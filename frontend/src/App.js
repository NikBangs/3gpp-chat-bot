import React, { useEffect, useState } from "react";
import Graph from "./Graph";
import Chat from "./Chat";

function App() {
  const [graphData, setGraphData] = useState({ nodes: [], links: [] });
  const [highlightedNodes, setHighlightedNodes] = useState([]);
  const [messages, setMessages] = useState([]);

  useEffect(() => {
    const fetchGraph = async () => {
      const res = await fetch("http://localhost:5000/api/graph");
      const data = await res.json();
      setGraphData(data);
    };
    fetchGraph();
  }, []);

  const handleSend = async (text) => {
    const newMessages = [...messages, { sender: "user", text }];
    setMessages(newMessages);

    try {
      const res = await fetch("http://localhost:5000/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: text }),
      });
      const data = await res.json();

      setMessages([
        ...newMessages,
        { sender: "assistant", text: data.answer },
      ]);
      setHighlightedNodes(data.highlight || []);
    } catch (err) {
      setMessages([
        ...newMessages,
        { sender: "assistant", text: "❌ Failed to fetch answer." },
      ]);
    }
  };

  return (
    <div className="app-container">
      <div className="graph-panel">
        <Graph graphData={graphData} highlightedNodes={highlightedNodes} />
      </div>
      <div className="chat-panel">
        <Chat messages={messages} onSend={handleSend} />
      </div>
    </div>
  );
}

export default App;
