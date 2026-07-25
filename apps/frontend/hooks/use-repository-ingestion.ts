"use client";

import { useMutation } from "@tanstack/react-query";

import { ingestRepository } from "@/services/repository.service";
import { RepositorySource } from "@/types/repository";

export function useRepositoryIngestion() {
  return useMutation({
    mutationFn: (source: RepositorySource) => ingestRepository(source),
  });
}
