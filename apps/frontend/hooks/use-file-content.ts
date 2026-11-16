import { useQuery } from "@tanstack/react-query";
import { fetchFileContent } from "@/services/repository.service";
import { FileContent } from "@/types/repository";

export function useFileContent(repositoryId?: string, filePath?: string) {
  return useQuery<FileContent>({
    queryKey: ["repository-file", repositoryId, filePath],
    queryFn: () => fetchFileContent(repositoryId!, filePath!),
    enabled: !!repositoryId && !!filePath,
  });
}
