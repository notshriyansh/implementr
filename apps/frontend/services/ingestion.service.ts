import { apiClient } from "./api-client";
import { IngestionResponse } from "@/types/paper";

export async function ingestPaper(
  pdfUrl: string,
  paperId: string,
): Promise<IngestionResponse> {
  const response = await apiClient.post("/ingestion/download", null, {
    params: {
      pdf_url: pdfUrl,
      paper_id: paperId,
    },
  });

  return response.data;
}
