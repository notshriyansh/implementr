"use client";

import { useQuery } from "@tanstack/react-query";

import { searchSymbols } from "@/services/symbol.service";

export function useSymbolSearch(query: string) {
  return useQuery({
    queryKey: ["symbol-search", query],
    queryFn: () => searchSymbols(query),
    enabled: query.length > 1,
  });
}
