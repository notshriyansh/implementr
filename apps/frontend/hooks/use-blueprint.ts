import { useMutation } from "@tanstack/react-query";
import type { ImplementationBlueprint } from "@/types/repository";
import { generateBlueprint } from "@/services/blueprint.service";

interface BlueprintInput {
  question: string;
  repositoryId?: string;
}

export function useBlueprint() {
  return useMutation<ImplementationBlueprint, Error, BlueprintInput>({
    mutationFn: ({ question, repositoryId }) =>
      generateBlueprint(question, repositoryId),
  });
}
