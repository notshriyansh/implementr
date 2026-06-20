"use client";

import { useMutation } from "@tanstack/react-query";
import { askPaperQuestion } from "@/services/chat.service";

export function usePaperChat() {
  return useMutation({
    mutationFn: ({
      sessionId,
      question,
    }: {
      sessionId: string;
      question: string;
    }) => askPaperQuestion(sessionId, question),
  });
}
