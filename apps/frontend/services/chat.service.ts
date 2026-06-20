import { apiClient } from "./api-client";
import { ChatResponse } from "@/types/paper";

export async function askPaperQuestion(
  sessionId: string,
  question: string,
): Promise<ChatResponse> {
  const response = await apiClient.post("/chat", null, {
    params: {
      session_id: sessionId,
      question,
    },
  });

  return response.data;
}
