import { useQuery } from "@tanstack/react-query";
import { fetchFileContent } from "@/services/repository.service";
import { FileContent } from "@/types/repository";

export function useFileContent(repoPath?: string, filePath?: string) {
  return useQuery<FileContent>({
    queryKey: ["repository-file", repoPath, filePath],
    queryFn: () => fetchFileContent(repoPath!, filePath!),
    enabled: !!repoPath && !!filePath,
  });
}
