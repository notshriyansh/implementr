import { apiClient } from "./api-client";
import { ResearchReproductionPlan } from "@/types/repository";

export async function generateReproductionPlan(
  question: string,
): Promise<ResearchReproductionPlan> {
  const response = await apiClient.post("/reproduction/plan", null, {
    params: {
      question,
    },
  });

  return response.data;
}
