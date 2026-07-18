"use client";

import { useMutation } from "@tanstack/react-query";

import { createWorkspace } from "@/services/workspace.service";

export function useSaveWorkspace() {
  return useMutation({
    mutationFn: createWorkspace,
  });
}
