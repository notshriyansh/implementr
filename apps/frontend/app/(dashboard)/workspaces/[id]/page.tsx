"use client";

import { useParams } from "next/navigation";
import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";

import { PageContainer } from "@/components/shared/page-container";

import { useWorkspace } from "@/hooks/use-workspace";
import { useWorkspaceOutputs } from "@/hooks/use-workspace-outputs";

import { useAppStore } from "@/stores/app-store";

export default function WorkspaceDetailPage() {
  const params = useParams();

  const router = useRouter();

  const workspaceId = params.id as string;

  const workspaceQuery = useWorkspace(workspaceId);

  const outputsQuery = useWorkspaceOutputs(workspaceId);

  const hydrateWorkspace = useAppStore((state) => state.hydrateWorkspace);

  if (workspaceQuery.isLoading || outputsQuery.isLoading) {
    return (
      <PageContainer>
        <div className="text-muted-foreground">Loading workspace...</div>
      </PageContainer>
    );
  }

  if (!workspaceQuery.data) {
    return (
      <PageContainer>
        <div className="text-muted-foreground">Workspace not found.</div>
      </PageContainer>
    );
  }

  const workspace = workspaceQuery.data;

  const outputs = outputsQuery.data;

  function handleResume() {
    hydrateWorkspace({
      workspaceId: workspace.id,
      workspaceName: workspace.name,
      selectedRepository: workspace.selected_repository,
      workspaceQuestion: workspace.workspace_question,
      blueprintTargetFile: workspace.blueprint_target_file,
      blueprintTargetSymbol: workspace.blueprint_target_symbol,
      blueprintTargetReason: workspace.blueprint_target_reason,
    });

    router.push("/workspace");
  }

  return (
    <PageContainer>
      <section className="mb-8">
        <div className="mb-4 text-xs uppercase tracking-[0.25em] text-muted-foreground">
          SESSION
        </div>

        <h1 className="text-3xl font-semibold tracking-tight lg:text-4xl">
          {workspace.name}
        </h1>

        <p className="mt-4 text-muted-foreground">
          Resume a previously saved implementation session.
        </p>
      </section>

      <div className="rounded-lg border border-border bg-card p-6">
        <div className="space-y-4">
          <div>
            <div className="text-xs uppercase text-muted-foreground">
              Repository
            </div>

            <div className="mt-1">
              {workspace.selected_repository ?? "None"}
            </div>
          </div>

          <div>
            <div className="text-xs uppercase text-muted-foreground">
              Question
            </div>

            <div className="mt-1">{workspace.workspace_question ?? "None"}</div>
          </div>

          <div>
            <div className="text-xs uppercase text-muted-foreground">
              Blueprint Target
            </div>

            <div className="mt-1">
              {workspace.blueprint_target_symbol ?? "None"}
            </div>
          </div>
        </div>
      </div>

      <div className="mt-6 rounded-lg border border-border bg-card p-6">
        <h2 className="mb-4 font-semibold">Generated Outputs</h2>

        <div className="space-y-3 text-sm">
          {[
            { label: "Hybrid Analysis", done: !!outputs?.hybrid_result },
            { label: "Reproduction Plan", done: !!outputs?.reproduction_result },
            { label: "Blueprint", done: !!outputs?.blueprint_result },
            { label: "Evaluation", done: !!outputs?.evaluation_result },
          ].map((item) => (
            <div key={item.label} className="flex items-center gap-3">
              <div
                className={`h-2 w-2 rounded-full shrink-0 ${
                  item.done ? "bg-green-500" : "bg-muted-foreground/30"
                }`}
              />
              <span className={item.done ? "text-foreground" : "text-muted-foreground"}>
                {item.label}
              </span>
              {item.done && (
                <span className="ml-auto text-xs text-green-500/80">Complete</span>
              )}
            </div>
          ))}
        </div>
      </div>

      <div className="mt-6">
        <Button onClick={handleResume}>Resume Workspace</Button>
      </div>
    </PageContainer>
  );
}
