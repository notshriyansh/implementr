"use client";

import { useQuery } from "@tanstack/react-query";

import { listWorkspaces } from "@/services/workspace.service";

export function useWorkspaces() {
  return useQuery({
    queryKey: ["workspaces"],
    queryFn: listWorkspaces,
  });
}
