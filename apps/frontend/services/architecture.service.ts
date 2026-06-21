import { apiClient } from "./api-client";

export async function analyzeArchitecture(query: string) {
  const response = await apiClient.post("/architecture/analyze", null, {
    params: { query },
  });

  return response.data;
}
