"use client";

import { useMutation } from "@tanstack/react-query";

import { generateReproductionPlan } from "@/services/reproduction.service";

export function useReproductionPlan() {
  return useMutation({
    mutationFn: (question: string) => generateReproductionPlan(question),
  });
}
