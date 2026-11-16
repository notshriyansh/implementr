import { apiClient } from "./api-client";
import { HybridAnalysisResponse } from "@/types/repository";

export async function analyzeHybrid(
  question: string,
  repositoryId?: string,
  paperId?: string,
): Promise<HybridAnalysisResponse> {
  const response = await apiClient.post("/hybrid/analyze", null, {
    params: {
      question,
      repository_id: repositoryId,
      paper_id: paperId,
    },
  });

  return response.data;
}
