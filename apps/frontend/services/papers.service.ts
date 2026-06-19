import { apiClient } from "./api-client";
import { PaperSearchResponse } from "@/types/paper";

export async function searchPapers(
  query: string,
): Promise<PaperSearchResponse> {
  const response = await apiClient.get("/papers/search", {
    params: { query },
  });

  return response.data;
}
