"use client";

import { useMutation } from "@tanstack/react-query";

import { ingestRepository } from "@/services/repository.service";

export function useRepositoryIngestion() {
  return useMutation({
    mutationFn: (repoPath: string) => ingestRepository(repoPath),
  });
}
