"use client";

import { useQuery } from "@tanstack/react-query";

import { getWorkspace } from "@/services/workspace.service";

export function useWorkspace(workspaceId: string) {
  return useQuery({
    queryKey: ["workspace", workspaceId],
    queryFn: () => getWorkspace(workspaceId),
    enabled: !!workspaceId,
  });
}
