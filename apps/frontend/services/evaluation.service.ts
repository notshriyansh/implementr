import { apiClient } from "./api-client";
import { BlueprintEvaluationResult } from "@/types/repository";

export async function evaluateBlueprint(
  question: string,
): Promise<BlueprintEvaluationResult> {
  const response = await apiClient.get("/evaluation/blueprint", {
    params: {
      question,
    },
  });

  return response.data;
}
