"use client";

import { FileText, FolderGit2, Target, MessageSquare } from "lucide-react";

import { useAppStore } from "@/stores/app-store";

export function ContextPanel() {
  const selectedPaper = useAppStore((state) => state.selectedPaper);

  const selectedRepository = useAppStore((state) => state.selectedRepository);

  const workspaceQuestion = useAppStore((state) => state.workspaceQuestion);

  const blueprintTargetSymbol = useAppStore(
    (state) => state.blueprintTargetSymbol,
  );

  return (
    <div className="rounded-lg border border-border bg-card p-4">
      <h3 className="mb-4 text-xs font-semibold uppercase tracking-wider text-muted-foreground">
        Active Context
      </h3>

      <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-4">
        <ContextItem
          icon={<FileText className="h-4 w-4" />}
          label="Paper"
          value={selectedPaper?.title ?? "No paper selected"}
        />

        <ContextItem
          icon={<FolderGit2 className="h-4 w-4" />}
          label="Repository"
          value={selectedRepository ?? "No repository selected"}
        />

        <ContextItem
          icon={<MessageSquare className="h-4 w-4" />}
          label="Question"
          value={workspaceQuestion ?? "No active question"}
        />

        <ContextItem
          icon={<Target className="h-4 w-4" />}
          label="Blueprint Target"
          value={blueprintTargetSymbol ?? "No target selected"}
        />
      </div>
    </div>
  );
}

function ContextItem({
  icon,
  label,
  value,
}: {
  icon: React.ReactNode;
  label: string;
  value: string;
}) {
  return (
    <div className="rounded-lg bg-muted/50 p-4">
      <div className="flex items-center gap-2 text-sm text-muted-foreground">
        {icon}
        {label}
      </div>

      <div className="mt-2 wrap-break-word text-sm font-medium">{value}</div>
    </div>
  );
}
