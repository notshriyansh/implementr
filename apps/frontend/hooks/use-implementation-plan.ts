"use client";

import { useMutation } from "@tanstack/react-query";
import { generateImplementationPlan } from "@/services/plan.service";

export function useImplementationPlan() {
  return useMutation({
    mutationFn: (question: string) => generateImplementationPlan(question),
  });
}
