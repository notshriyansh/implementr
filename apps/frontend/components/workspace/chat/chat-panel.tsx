"use client";

import { useState } from "react";

import { ChatMessage } from "./chat-message";
import { ChatInput } from "./chat-input";

import { ChatMessage as Message } from "@/types/chat";

import { streamPaperChat } from "@/services/stream-chat.service";

export function ChatPanel() {
  const [messages, setMessages] = useState<Message[]>([]);

  const [streaming, setStreaming] = useState(false);

  async function handleSend(question: string) {
    const userMessage: Message = {
      id: crypto.randomUUID(),
      role: "user",
      content: question,
    };

    const assistantId = crypto.randomUUID();

    setMessages((prev) => [
      ...prev,
      userMessage,
      {
        id: assistantId,
        role: "assistant",
        content: "",
      },
    ]);

    setStreaming(true);

    try {
      await streamPaperChat("research-session", question, (chunk) => {
        setMessages((prev) =>
          prev.map((message) =>
            message.id === assistantId
              ? {
                  ...message,
                  content: message.content + chunk,
                }
              : message,
          ),
        );
      });
    } finally {
      setStreaming(false);
    }
  }

  return (
    <div className="flex flex-col h-[70vh] border rounded-xl">
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {messages.map((message) => (
          <ChatMessage key={message.id} message={message} />
        ))}
      </div>

      <ChatInput onSend={handleSend} disabled={streaming} />
    </div>
  );
}
