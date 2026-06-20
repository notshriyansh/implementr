import { apiClient } from "./api-client";
import { ImplementationPlanResponse } from "@/types/paper";

export async function generateImplementationPlan(
  question: string,
): Promise<ImplementationPlanResponse> {
  const response = await apiClient.post("/agents/implementation-plan", null, {
    params: {
      question,
    },
  });

  return response.data;
}
