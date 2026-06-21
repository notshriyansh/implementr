"use client";

import { useQuery } from "@tanstack/react-query";

import { getRepositoryStructure } from "@/services/repository.service";

export function useRepositoryStructure(repoPath: string, enabled = false) {
  return useQuery({
    queryKey: ["repository-structure", repoPath],
    queryFn: () => getRepositoryStructure(repoPath),
    enabled,
  });
}
