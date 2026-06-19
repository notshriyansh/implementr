"use client";

import { useQuery } from "@tanstack/react-query";
import { searchPapers } from "@/services/papers.service";

export function usePaperSearch(query: string) {
  return useQuery({
    queryKey: ["papers", query],
    queryFn: () => searchPapers(query),
    enabled: query.length > 0,
  });
}
