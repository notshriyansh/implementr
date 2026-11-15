import { apiClient } from "./api-client";
import { ImplementationBlueprint } from "@/types/repository";

export async function generateBlueprint(
  question: string,
  repositoryId?: string,
): Promise<ImplementationBlueprint> {
  const response = await apiClient.get("/blueprints/generate", {
    params: {
      question,
      repository_id: repositoryId,
    },
  });

  return response.data;
}
