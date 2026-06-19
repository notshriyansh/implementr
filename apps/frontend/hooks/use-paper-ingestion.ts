"use client";

import { useMutation } from "@tanstack/react-query";
import { ingestPaper } from "@/services/ingestion.service";

export function usePaperIngestion() {
  return useMutation({
    mutationFn: ({ pdfUrl, paperId }: { pdfUrl: string; paperId: string }) =>
      ingestPaper(pdfUrl, paperId),
  });
}
