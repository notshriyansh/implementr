import { apiClient } from "./api-client";

import {
  RepositoryMap,
  FileContent,
  RepositoryIngestResponse,
} from "@/types/repository";

export async function ingestRepository(
  location: string,
): Promise<RepositoryIngestResponse> {
  const response = await apiClient.post("/repository/ingest", null, {
    params: { location },
  });

  return response.data;
}

export async function getRepositoryStructure(
  repositoryId: string,
): Promise<RepositoryMap> {
  const response = await apiClient.get("/repository/structure", {
    params: { repository_id: repositoryId },
  });

  return response.data;
}

export async function searchRepository(query: string) {
  const response = await apiClient.get("/repository/search", {
    params: { query },
  });

  return response.data;
}

export async function fetchFileContent(
  repositoryId: string,
  filePath: string,
): Promise<FileContent> {
  const response = await apiClient.get("/repository/file", {
    params: {
      repository_id: repositoryId,
      file_path: filePath,
    },
  });

  return response.data;
}
