// src/App.js
import React, { useState } from "react";
import axios from "axios";
import "./App.css"; // We'll use this for styling

function App() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessages = [...messages, { role: "user", text: input }];
    setMessages(newMessages);
    setInput("");

    try {
      const res = await axios.post("http://localhost:8000/chat", { text: input });
      const reply = res.data.response || res.data.error || "No response.";
      setMessages((prev) => [...prev, { role: "ai", text: reply }]);
    } catch (error) {
      console.error("Error:", error);
      setMessages((prev) => [...prev, { role: "ai", text: "Error contacting the server." }]);
    }
  };

  return (
    <div className="app">
      <div className="chat-box">
        <h1>Heritage Square AI Assistant</h1>
        <div className="messages">
          {messages.map((msg, i) => (
            <div key={i} className={`message ${msg.role}`}>
              <div className="bubble">{msg.text}</div>
            </div>
          ))}
        </div>
        <div className="input-row">
          <input
            type="text"
            placeholder="Ask me to read, list, move or tag a file..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button onClick={sendMessage}>Send</button>
        </div>
      </div>
    </div>
  );
}

export default App;
