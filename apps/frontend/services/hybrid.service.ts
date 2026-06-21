import { apiClient } from "./api-client";
import { HybridAnalysisResponse } from "@/types/repository";

export async function analyzeHybrid(
  question: string,
): Promise<HybridAnalysisResponse> {
  const response = await apiClient.post("/hybrid/analyze", null, {
    params: {
      question,
    },
  });

  return response.data;
}
