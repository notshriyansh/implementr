"use client";

import { useState } from "react";

import Link from "next/link";
import { useAppStore } from "@/stores/app-store";

import { Button } from "@/components/ui/button";
import { Check, X, Loader2 } from "lucide-react";

import { EmptyState } from "@/components/shared/empty-state";
import { PageContainer } from "@/components/shared/page-container";

import { ContextPanel } from "@/components/context/context-panel";

import { HybridQuery } from "@/components/workspace/hybrid-query";
import { HybridResult } from "@/components/workspace/hybrid-result";

import { ReproductionResult } from "@/components/reproduction/reproduction-result";
import { BlueprintResult } from "@/components/blueprints/blueprint-result";
import { EvaluationResult } from "@/components/evaluation/evaluation-result";

import { useHybridAnalysis } from "@/hooks/use-hybrid-analysis";
import { useReproductionPlan } from "@/hooks/use-reproduction-plan";
import { useBlueprint } from "@/hooks/use-blueprint";
import { useBlueprintEvaluation } from "@/hooks/use-blueprint-evaluation";
import { WorkspacePipeline } from "@/components/workspace/workspace-pipeline";
import { useSaveWorkspace } from "@/hooks/use-save-workspace";
import { useWorkspaceOutputs } from "@/hooks/use-workspace-outputs";
import { saveWorkspaceOutputs } from "@/services/workspace.service";

export default function WorkspacePage() {
  const [question, setQuestion] = useState(
    () => useAppStore.getState().workspaceQuestion ?? "",
  );

  const hybridMutation = useHybridAnalysis();
  const reproductionMutation = useReproductionPlan();
  const blueprintMutation = useBlueprint();
  const evaluationMutation = useBlueprintEvaluation();

  const selectedPaper = useAppStore((state) => state.selectedPaper);
  const selectedRepository = useAppStore((state) => state.selectedRepository);
  const selectedRepositoryId = useAppStore(
    (state) => state.selectedRepositoryId,
  );
  const workspaceId = useAppStore((state) => state.workspaceId);
  const setWorkspaceId = useAppStore((state) => state.setWorkspaceId);
  const setWorkspaceName = useAppStore((state) => state.setWorkspaceName);

  const workspaceOutputsQuery = useWorkspaceOutputs(workspaceId ?? "");
  const saveWorkspaceMutation = useSaveWorkspace();

  const workspaceReady =
    !!selectedRepository && (!!selectedPaper || !!workspaceId);

  const hybridResult =
    hybridMutation.data ?? workspaceOutputsQuery.data?.hybrid_result ?? null;

  const reproductionResult =
    reproductionMutation.data ??
    workspaceOutputsQuery.data?.reproduction_result ??
    null;

  const blueprintResult =
    blueprintMutation.data ??
    workspaceOutputsQuery.data?.blueprint_result ??
    null;

  const evaluationResult =
    evaluationMutation.data ??
    workspaceOutputsQuery.data?.evaluation_result ??
    null;

  async function persistWorkspaceOutput(
    field:
      | "hybrid_result"
      | "reproduction_result"
      | "blueprint_result"
      | "evaluation_result",
    result: unknown,
  ) {
    if (!workspaceId || !result) {
      return;
    }

    await saveWorkspaceOutputs({
      workspace_id: workspaceId,
      [field]: result,
    });

    await workspaceOutputsQuery.refetch();
  }

  async function handleSaveWorkspace() {
    let currentWorkspaceId = workspaceId;

    if (!currentWorkspaceId) {
      const workspace = await saveWorkspaceMutation.mutateAsync({
        name: question || "Untitled Workspace",
        selected_repository: selectedRepository,
        selected_repository_id: selectedRepositoryId,
        selected_paper: selectedPaper?.title,
        workspace_question: question,
        blueprint_target_file: useAppStore.getState().blueprintTargetFile,
        blueprint_target_symbol: useAppStore.getState().blueprintTargetSymbol,
        blueprint_target_reason: useAppStore.getState().blueprintTargetReason,
      });

      currentWorkspaceId = workspace.id;
      setWorkspaceId(workspace.id);
      setWorkspaceName(workspace.name);
    }

    const currentResults = [
      ["hybrid_result", hybridResult],
      ["reproduction_result", reproductionResult],
      ["blueprint_result", blueprintResult],
      ["evaluation_result", evaluationResult],
    ] as const;

    const outputs = Object.fromEntries(
      currentResults.filter(([, result]) => result != null),
    );

    if (Object.keys(outputs).length > 0) {
      await saveWorkspaceOutputs({
        workspace_id: currentWorkspaceId,
        ...outputs,
      });

      await workspaceOutputsQuery.refetch();
    }
  }

  return (
    <PageContainer>
      <section className="mb-8">
        <div className="mb-4 text-xs uppercase tracking-[0.25em] text-muted-foreground">
          04 · WORKSPACE
        </div>

        <div className="flex items-start justify-between gap-4">
          <div>
            <h1 className="text-3xl font-semibold tracking-tight lg:text-4xl">
              Implementation Workspace
            </h1>

            <p className="mt-4 max-w-3xl text-base leading-7 text-muted-foreground">
              Move from research understanding to implementation planning,
              reproduction analysis, blueprint generation and evaluation.
            </p>
          </div>

          <Button
            variant="outline"
            onClick={handleSaveWorkspace}
            disabled={saveWorkspaceMutation.isPending}
          >
            {saveWorkspaceMutation.isPending ? (
              <>
                <Loader2 className="h-4 w-4 animate-spin" />
                Saving
              </>
            ) : (
              "Save Workspace"
            )}
          </Button>
        </div>
      </section>

      <ContextPanel />

      {!workspaceReady && (
        <div className="mt-8 rounded-lg border border-border bg-card p-6">
          <h2 className="mb-6 text-lg font-semibold">Workspace Requirements</h2>

          <div className="space-y-3">
            <div className="flex items-center gap-3">
              {selectedPaper ? (
                <div
                  className="flex h-5 w-5 items-center justify-center rounded-full bg-green-500/10"
                  aria-label="Completed"
                >
                  <Check className="h-3 w-3 text-green-500" />
                </div>
              ) : (
                <div
                  className="flex h-5 w-5 items-center justify-center rounded-full bg-muted"
                  aria-label="Not completed"
                >
                  <X className="h-3 w-3 text-muted-foreground" />
                </div>
              )}
              <span className="text-sm">Research Paper Selected</span>
            </div>

            <div className="flex items-center gap-3">
              {selectedRepository ? (
                <div
                  className="flex h-5 w-5 items-center justify-center rounded-full bg-green-500/10"
                  aria-label="Completed"
                >
                  <Check className="h-3 w-3 text-green-500" />
                </div>
              ) : (
                <div
                  className="flex h-5 w-5 items-center justify-center rounded-full bg-muted"
                  aria-label="Not completed"
                >
                  <X className="h-3 w-3 text-muted-foreground" />
                </div>
              )}
              <span className="text-sm">Repository Indexed</span>
            </div>
          </div>

          <div className="mt-6 flex gap-3">
            {!selectedPaper && (
              <Button asChild>
                <Link href="/research">Go To Research</Link>
              </Button>
            )}

            {!selectedRepository && (
              <Button asChild variant="outline">
                <Link href="/repository">Go To Repository</Link>
              </Button>
            )}
          </div>
        </div>
      )}

      {workspaceReady && (
        <>
          <div className="mt-8">
            <WorkspacePipeline
              hybridReady={!!hybridResult}
              reproductionReady={!!reproductionResult}
              blueprintReady={!!blueprintResult}
              evaluationReady={!!evaluationResult}
            />
          </div>

          <div className="mt-8">
            <HybridQuery
              loading={hybridMutation.isPending}
              onAnalyze={async (inputQuestion) => {
                setQuestion(inputQuestion);

                const result = await hybridMutation.mutateAsync({
                  question: inputQuestion,
                  repositoryId: selectedRepositoryId,
                  paperId: selectedPaper?.paper_id,
                });

                await persistWorkspaceOutput("hybrid_result", result);
              }}
            />
          </div>

          {!hybridResult && (
            <div className="mt-10">
              <EmptyState
                title="Ready for analysis"
                description="Ask a repository-aware implementation question to generate implementation guidance."
              />
            </div>
          )}

          {hybridResult && (
            <div className="mt-10 space-y-10">
              <HybridResult result={hybridResult} />

              {!reproductionResult && (
                <div className="rounded-lg border border-border bg-card p-6">
                  <h2 className="mb-3 text-lg font-semibold">
                    Research Reproduction
                  </h2>

                  <p className="mb-6 text-sm text-muted-foreground">
                    Analyze concept mappings, architecture gaps and modification
                    targets for this implementation.
                  </p>

                  <Button
                    onClick={async () => {
                      const result = await reproductionMutation.mutateAsync({
                        question,
                        repositoryId: selectedRepositoryId,
                        paperId: selectedPaper?.paper_id,
                      });
                      await persistWorkspaceOutput(
                        "reproduction_result",
                        result,
                      );
                    }}
                    disabled={reproductionMutation.isPending}
                  >
                    {reproductionMutation.isPending ? (
                      <>
                        <Loader2 className="h-4 w-4 animate-spin" />
                        Generating
                      </>
                    ) : (
                      "Generate Reproduction Plan"
                    )}
                  </Button>
                </div>
              )}

              {reproductionResult && (
                <>
                  <ReproductionResult result={reproductionResult} />

                  {!blueprintResult && (
                    <div className="rounded-lg border border-border bg-card p-6">
                      <h2 className="mb-3 text-lg font-semibold">
                        Implementation Blueprint
                      </h2>

                      <p className="mb-6 text-sm text-muted-foreground">
                        Generate exact file-level implementation instructions.
                      </p>

                      <Button
                        onClick={async () => {
                          const result = await blueprintMutation.mutateAsync({
                            question,
                            repositoryId: selectedRepositoryId,
                          });
                          await persistWorkspaceOutput(
                            "blueprint_result",
                            result,
                          );
                        }}
                        disabled={blueprintMutation.isPending}
                      >
                        {blueprintMutation.isPending ? (
                          <>
                            <Loader2 className="h-4 w-4 animate-spin" />
                            Generating
                          </>
                        ) : (
                          "Generate Blueprint"
                        )}
                      </Button>
                    </div>
                  )}
                </>
              )}

              {blueprintResult && (
                <>
                  <BlueprintResult result={blueprintResult} />

                  {!evaluationResult && (
                    <div className="rounded-lg border border-border bg-card p-6">
                      <h2 className="mb-3 text-lg font-semibold">
                        Blueprint Evaluation
                      </h2>

                      <p className="mb-6 text-sm text-muted-foreground">
                        Evaluate blueprint quality and implementation coverage.
                      </p>

                      <Button
                        onClick={async () => {
                          const result =
                            await evaluationMutation.mutateAsync(question);
                          await persistWorkspaceOutput(
                            "evaluation_result",
                            result,
                          );
                        }}
                        disabled={evaluationMutation.isPending}
                      >
                        {evaluationMutation.isPending ? (
                          <>
                            <Loader2 className="h-4 w-4 animate-spin" />
                            Evaluating
                          </>
                        ) : (
                          "Evaluate Blueprint"
                        )}
                      </Button>
                    </div>
                  )}
                </>
              )}

              {evaluationResult && (
                <EvaluationResult result={evaluationResult} />
              )}
            </div>
          )}
        </>
      )}
    </PageContainer>
  );
}
