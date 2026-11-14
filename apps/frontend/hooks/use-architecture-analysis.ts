"use client";

import { useMutation } from "@tanstack/react-query";
import { analyzeArchitecture } from "@/services/architecture.service";

interface ArchitectureAnalysisInput {
  query: string;
  repositoryId: string;
}

export function useArchitectureAnalysis() {
  return useMutation({
    mutationFn: ({ query, repositoryId }: ArchitectureAnalysisInput) =>
      analyzeArchitecture(query, repositoryId),
  });
}
