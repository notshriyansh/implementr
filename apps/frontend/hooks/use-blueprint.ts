"use client";

import { useMutation } from "@tanstack/react-query";

import { generateBlueprint } from "@/services/blueprint.service";

import { ImplementationBlueprint } from "@/types/repository";

export function useBlueprint() {
  return useMutation<ImplementationBlueprint, Error, string>({
    mutationFn: generateBlueprint,
  });
}
