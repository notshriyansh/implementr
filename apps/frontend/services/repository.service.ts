import { apiClient } from "./api-client";

export async function ingestRepository(repoPath: string) {
  const response = await apiClient.post("/repository/ingest", null, {
    params: {
      repo_path: repoPath,
    },
  });

  return response.data;
}

export async function getRepositoryStructure(repoPath: string) {
  const response = await apiClient.get("/repository/structure", {
    params: {
      repo_path: repoPath,
    },
  });

  return response.data;
}

export async function searchRepository(query: string) {
  const response = await apiClient.get("/repository/search", {
    params: { query },
  });

  return response.data;
}

export async function fetchFileContent(repoPath: string, filePath: string) {
  const response = await apiClient.get("/repository/file", {
    params: { repo_path: repoPath, file_path: filePath },
  });

  return response.data;
}
