import { apiClient } from "./api-client";

export async function analyzeArchitecture(query: string, repositoryId: string) {
  const response = await apiClient.post("/architecture/analyze", null, {
    params: {
      query,
      repository_id: repositoryId,
    },
  });

  return response.data;
}
