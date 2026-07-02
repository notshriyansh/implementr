"use client";

import { CheckCircle2, FileText, FolderGit2 } from "lucide-react";

import { useAppStore } from "@/stores/app-store";

export function ContextPanel() {
  const selectedPaper = useAppStore((state) => state.selectedPaper);

  const selectedRepository = useAppStore((state) => state.selectedRepository);

  return (
    <div
      className="
        rounded-xl
        border
        border-border
        bg-card
        p-5
      "
    >
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
          icon={<CheckCircle2 className="h-4 w-4 text-green-500" />}
          label="Repository Indexed"
          value={selectedRepository ? "Ready" : "Not Available"}
        />

        <ContextItem
          icon={<CheckCircle2 className="h-4 w-4 text-green-500" />}
          label="Architecture"
          value={selectedRepository ? "Ready" : "Unavailable"}
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
      <div className="flex items-center gap-2 text-muted-foreground text-sm">
        {icon}
        {label}
      </div>

      <div className="mt-2 text-sm font-medium wrap-break-word">{value}</div>
    </div>
  );
}
