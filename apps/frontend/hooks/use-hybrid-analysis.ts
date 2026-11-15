"use client";

import { useMutation } from "@tanstack/react-query";

import { analyzeHybrid } from "@/services/hybrid.service";

export function useHybridAnalysis() {
  return useMutation({
    mutationFn: ({
      question,
      repositoryId,
    }: {
      question: string;
      repositoryId?: string;
    }) => analyzeHybrid(question, repositoryId),
  });
}
