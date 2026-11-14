import { apiClient } from "./api-client";
import { ResearchReproductionPlan } from "@/types/repository";

export async function generateReproductionPlan(
  question: string,
  repositoryId?: string,
  paperId?: string,
): Promise<ResearchReproductionPlan> {
  const response = await apiClient.post("/reproduction/plan", null, {
    params: {
      question,
      repository_id: repositoryId,
      paper_id: paperId,
    },
  });

  return response.data;
}
