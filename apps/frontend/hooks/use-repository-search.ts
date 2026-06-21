"use client";

import { useQuery } from "@tanstack/react-query";

import { searchRepository } from "@/services/repository.service";

export function useRepositorySearch(query: string) {
  return useQuery({
    queryKey: ["repository-search", query],
    queryFn: () => searchRepository(query),
    enabled: query.length > 1,
  });
}
