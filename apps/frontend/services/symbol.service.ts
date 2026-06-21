import { apiClient } from "./api-client";

export async function searchSymbols(query: string) {
  const response = await apiClient.get("/symbols/search", {
    params: { query },
  });

  return response.data;
}
