"use client";

import { useQuery } from "@tanstack/react-query";

import { getWorkspaceOutputs } from "@/services/workspace.service";

export function useWorkspaceOutputs(workspaceId: string) {
  return useQuery({
    queryKey: ["workspace-outputs", workspaceId],
    queryFn: () => getWorkspaceOutputs(workspaceId),
    enabled: !!workspaceId,
  });
}
