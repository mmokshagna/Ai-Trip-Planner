import { useCallback, useState } from "react";
import { sendChatMessage } from "../utils/api";
import { ItineraryResponse } from "./useItinerary";

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

export function useChat(itinerary?: ItineraryResponse | null, persona?: string) {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [isSending, setIsSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (content: string) => {
      const userMessage: ChatMessage = {
        id: generateId(),
        role: "user",
        content,
      };

      setMessages((previous) => [...previous, userMessage]);
      setIsSending(true);
      setError(null);

      try {
        const contextPayload: Record<string, unknown> | undefined = itinerary
          ? { itinerary }
          : persona
            ? { persona }
            : undefined;

        const response = await sendChatMessage({
          message: content,
          context: contextPayload,
        });

        const assistantMessage: ChatMessage = {
          id: generateId(),
          role: "assistant",
          content: response.data.message ?? "",
        };

        setMessages((previous) => [...previous, assistantMessage]);
      } catch (caughtError) {
        const assistantMessage: ChatMessage = {
          id: generateId(),
          role: "assistant",
          content: "I couldn't reach the travel companion. Please try again soon.",
        };
        const errorMessage =
          caughtError instanceof Error
            ? caughtError.message
            : "Unable to contact travel companion";
        setError(errorMessage);
        setMessages((previous) => [...previous, assistantMessage]);
      } finally {
        setIsSending(false);
      }
    },
    [itinerary, persona]
  );

  return {
    messages,
    isSending,
    error,
    sendMessage,
  };
}
