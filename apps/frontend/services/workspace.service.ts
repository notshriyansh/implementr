import { apiClient } from "./api-client";

import {
  Workspace,
  CreateWorkspaceRequest,
  WorkspaceOutput,
} from "@/types/workspace";

export async function createWorkspace(
  payload: CreateWorkspaceRequest,
): Promise<Workspace> {
  const response = await apiClient.post("/workspaces", payload);

  return response.data;
}

export async function listWorkspaces(): Promise<Workspace[]> {
  const response = await apiClient.get("/workspaces");

  return response.data;
}

export async function getWorkspace(workspaceId: string): Promise<Workspace> {
  const response = await apiClient.get(`/workspaces/${workspaceId}`);

  return response.data;
}

export async function saveWorkspaceOutputs(payload: {
  workspace_id: string;

  hybrid_result?: unknown;
  reproduction_result?: unknown;
  blueprint_result?: unknown;
  evaluation_result?: unknown;
}): Promise<WorkspaceOutput> {
  const response = await apiClient.post("/workspace-outputs", payload);

  return response.data;
}

export async function getWorkspaceOutputs(
  workspaceId: string,
): Promise<WorkspaceOutput> {
  const response = await apiClient.get(`/workspace-outputs/${workspaceId}`);

  return response.data;
}
