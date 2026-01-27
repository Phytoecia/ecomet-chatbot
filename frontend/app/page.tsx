"use client";

import { useState, useRef, useEffect } from "react";
import { Send, User, Bot, Loader2 } from "lucide-react";
import clsx from "clsx";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Message {
  role: "user" | "bot";
  content: string;
}

export default function Home() {
  const [messages, setMessages] = useState<Message[]>([
    { role: "bot", content: "Hello! I'm the eCOMET assistant. Ask me about installation, data input, or analysis workflows." }
  ]);
  const [input, setInput] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || isLoading) return;

    const userMessage = input.trim();
    setMessages((prev) => [...prev, { role: "user", content: userMessage }]);
    setInput("");
    setIsLoading(true);

    // Zero-config URL for Hugging Face Backend
    const baseUrl = process.env.NODE_ENV === "production"
      ? "https://phytoecia-ecomet-chatbot-backend.hf.space"
      : "http://localhost:8000";

    try {
      const response = await fetch(`${baseUrl}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage }),
      });

      if (!response.ok) throw new Error("Failed to fetch response");

      const data = await response.json();
      setMessages((prev) => [...prev, { role: "bot", content: data.response }]);
    } catch (error) {
      setMessages((prev) => [...prev, { role: "bot", content: "Sorry, something went wrong. Please ensure the backend is running." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-screen font-sans bg-white text-lg">
      {/* Navbar matched to eCOMET site */}
      <nav className="bg-navbar border-b border-gray-200 px-8 py-4 flex items-center shadow-sm">
        <h1 className="text-2xl font-bold tracking-tight text-primary">eCOMET chatbot</h1>
      </nav>

      {/* Chat Area */}
      <div className="flex-1 overflow-y-auto p-4 sm:p-8">
        <div className="max-w-3xl mx-auto space-y-6">
          {messages.map((msg, idx) => (
            <div
              key={idx}
              className={clsx(
                "flex items-start gap-4",
                msg.role === "user" ? "flex-row-reverse" : "flex-row"
              )}
            >
              <div className={clsx(
                "w-8 h-8 rounded-full flex items-center justify-center shrink-0",
                msg.role === "user" ? "bg-primary" : "bg-gray-200"
              )}>
                {msg.role === "user" ? <User className="w-5 h-5 text-white" /> : <Bot className="w-5 h-5 text-[#222222]" />}
              </div>

              <div className={clsx(
                "p-4 rounded-lg leading-relaxed max-w-[85%]",
                msg.role === "user"
                  ? "bg-primary text-white rounded-tr-none"
                  : "bg-navbar text-[#222222] rounded-tl-none border border-gray-100 prose max-w-none prose-base prose-headings:font-bold prose-h1:text-2xl prose-h2:text-xl prose-a:text-primary prose-code:text-primary prose-pre:bg-gray-100 prose-pre:text-primary prose-pre:border prose-pre:border-gray-200"
              )}>
                {msg.role === "user" ? (
                  <p className="whitespace-pre-wrap">{msg.content}</p>
                ) : (
                  <ReactMarkdown
                    remarkPlugins={[remarkGfm]}
                    components={{
                      // Start links in new tab
                      a: ({ node, ...props }) => <a {...props} target="_blank" rel="noopener noreferrer" />
                    }}
                  >
                    {msg.content}
                  </ReactMarkdown>
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="flex items-center gap-2 text-gray-500 ml-12">
              <Loader2 className="w-4 h-4 animate-spin" />
              <span className="text-sm">Generating answer...</span>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </div>

      {/* Input Area */}
      <div className="p-4 bg-white">
        <div className="max-w-3xl mx-auto relative flex items-center mb-[15vh]">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
            placeholder="Ask a question about eCOMET..."
            className="w-full px-4 py-3 rounded-lg border border-gray-300 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition-colors shadow-sm text-lg"
            disabled={isLoading}
          />
        </div>
        <p className="text-center text-xs text-gray-400 mt-[-10vh] mb-4">Powered by Gemini & eCOMET Documentation</p>
      </div>
    </div>
  );
}
