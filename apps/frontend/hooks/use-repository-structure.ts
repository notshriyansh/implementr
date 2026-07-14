"use client";

import { useQuery } from "@tanstack/react-query";

import { RepositoryMap } from "@/types/repository";

import { getRepositoryStructure } from "@/services/repository.service";

export function useRepositoryStructure(repoPath: string, enabled = false) {
  return useQuery<RepositoryMap>({
    queryKey: ["repository-structure", repoPath],
    queryFn: () => getRepositoryStructure(repoPath),
    enabled,
  });
}
