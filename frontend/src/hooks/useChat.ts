import { useCallback, useState } from "react";

interface ChatMessage {
  id: string;
  role: "user" | "assistant";
  content: string;
}

function generateId() {
  if (typeof crypto !== "undefined" && "randomUUID" in crypto) {
    return crypto.randomUUID();
  }
  return Math.random().toString(36).slice(2);
}

export function useChat() {
  const [messages, setMessages] = useState<ChatMessage[]>([]);

  const sendMessage = useCallback((content: string) => {
    const userMessage: ChatMessage = {
      id: generateId(),
      role: "user",
      content
    };

    const assistantMessage: ChatMessage = {
      id: generateId(),
      role: "assistant",
      content: "Sample response from GPT travel companion stub."
    };

    setMessages((previous) => [...previous, userMessage, assistantMessage]);
  }, []);

  return {
    messages,
    sendMessage
  };
}
