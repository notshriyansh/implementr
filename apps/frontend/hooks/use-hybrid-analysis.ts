"use client";

import { useMutation } from "@tanstack/react-query";

import { analyzeHybrid } from "@/services/hybrid.service";

export function useHybridAnalysis() {
  return useMutation({
    mutationFn: ({
      question,
      repositoryId,
      paperId,
    }: {
      question: string;
      repositoryId?: string;
      paperId?: string;
    }) => analyzeHybrid(question, repositoryId, paperId),
  });
}
