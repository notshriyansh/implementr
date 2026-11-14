import { useQuery } from "@tanstack/react-query";
import { getRepositoryStructure } from "@/services/repository.service";

export function useRepositoryStructure(repositoryId: string, enabled = false) {
  return useQuery({
    queryKey: ["repository-structure", repositoryId],
    queryFn: () => getRepositoryStructure(repositoryId),
    enabled: enabled && !!repositoryId,
  });
}
