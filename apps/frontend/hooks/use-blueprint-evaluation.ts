"use client";

import { useMutation } from "@tanstack/react-query";

import { evaluateBlueprint } from "@/services/evaluation.service";

import { BlueprintEvaluationResult } from "@/types/repository";

export function useBlueprintEvaluation() {
  return useMutation<BlueprintEvaluationResult, Error, string>({
    mutationFn: evaluateBlueprint,
  });
}
