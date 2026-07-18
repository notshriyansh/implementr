"use client";

import { PageContainer } from "@/components/shared/page-container";

import { WorkspaceCard } from "@/components/workspaces/workspace-card";
import { WorkspaceCardSkeleton } from "@/components/workspaces/workspace-card-skeleton";

import { useWorkspaces } from "@/hooks/use-workspaces";

export default function WorkspacesPage() {
  const workspacesQuery = useWorkspaces();

  return (
    <PageContainer>
      <section className="mb-8">
        <div className="mb-4 text-xs uppercase tracking-[0.25em] text-muted-foreground">
          05 · HISTORY
        </div>

        <h1 className="text-3xl font-semibold tracking-tight lg:text-4xl">
          Workspace History
        </h1>

        <p className="mt-4 text-muted-foreground">
          Browse and resume your previously saved implementation workspaces.
        </p>
      </section>

      {workspacesQuery.isPending && (
        <div className="grid gap-4">
          {Array.from({ length: 4 }).map((_, index) => (
            <WorkspaceCardSkeleton key={index} />
          ))}
        </div>
      )}

      {!workspacesQuery.isPending && workspacesQuery.data?.length === 0 && (
        <div className="rounded-lg border border-border bg-card p-8 text-center text-muted-foreground">
          No saved workspaces yet.
        </div>
      )}

      {!workspacesQuery.isPending && workspacesQuery.data && (
        <div className="grid gap-4">
          {workspacesQuery.data.map((workspace) => (
            <WorkspaceCard key={workspace.id} workspace={workspace} />
          ))}
        </div>
      )}
    </PageContainer>
  );
}
