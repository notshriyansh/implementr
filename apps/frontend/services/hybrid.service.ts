import { apiClient } from "./api-client";
import { HybridAnalysisResponse } from "@/types/repository";

export async function analyzeHybrid(
  question: string,
  repositoryId?: string,
): Promise<HybridAnalysisResponse> {
  const response = await apiClient.post("/hybrid/analyze", null, {
    params: {
      question,
      repository_id: repositoryId,
    },
  });

  return response.data;
}
