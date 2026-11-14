"use client";

import { useMutation } from "@tanstack/react-query";

import { generateReproductionPlan } from "@/services/reproduction.service";

export function useReproductionPlan() {
  return useMutation({
    mutationFn: ({
      question,
      repositoryId,
      paperId,
    }: {
      question: string;
      repositoryId?: string;
      paperId?: string;
    }) => generateReproductionPlan(question, repositoryId, paperId),
  });
}
