"use client";

import { useMutation } from "@tanstack/react-query";
import { analyzeArchitecture } from "@/services/architecture.service";

export function useArchitectureAnalysis() {
  return useMutation({
    mutationFn: (query: string) => analyzeArchitecture(query),
  });
}
