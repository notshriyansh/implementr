"use client";

import { useState } from "react";

import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";

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

export default function WorkspacePage() {
  const [question, setQuestion] = useState("");

  const hybridMutation = useHybridAnalysis();
  const reproductionMutation = useReproductionPlan();
  const blueprintMutation = useBlueprint();
  const evaluationMutation = useBlueprintEvaluation();

  return (
    <PageContainer>
      <section className="mb-12">
        <div className="mb-4 text-xs uppercase tracking-[0.25em] text-muted-foreground">
          04 · WORKSPACE
        </div>

        <h1 className="text-4xl font-semibold tracking-tighter sm:text-5xl lg:text-6xl">
          Implementation Workspace
        </h1>

        <p className="mt-5 max-w-3xl text-base leading-7 text-muted-foreground lg:text-lg lg:leading-8">
          Move from research understanding to implementation planning,
          reproduction analysis, blueprint generation and evaluation.
        </p>

        <div className="mt-6 flex flex-wrap gap-2">
          <Badge variant="secondary">Research</Badge>
          <Badge variant="secondary">Repository</Badge>
          <Badge variant="secondary">Architecture</Badge>
          <Badge variant="secondary">Blueprints</Badge>
          <Badge variant="secondary">Evaluation</Badge>
        </div>
      </section>

      <ContextPanel />

      <div className="mt-8">
        <HybridQuery
          loading={hybridMutation.isPending}
          onAnalyze={(inputQuestion) => {
            setQuestion(inputQuestion);
            hybridMutation.mutate(inputQuestion);
          }}
        />
      </div>

      {!hybridMutation.data && (
        <div className="mt-10">
          <EmptyState
            title="Ready for analysis"
            description="Ask a repository-aware implementation question to generate implementation guidance."
          />
        </div>
      )}

      {hybridMutation.data && (
        <div className="mt-10 space-y-10">
          <HybridResult result={hybridMutation.data} />

          {!reproductionMutation.data && (
            <div className="rounded-xl border border-border bg-card p-8">
              <h2 className="mb-3 text-lg font-semibold">
                Research Reproduction
              </h2>

              <p className="mb-6 text-muted-foreground">
                Analyze concept mappings, architecture gaps and modification
                targets for this implementation.
              </p>

              <Button
                onClick={() => reproductionMutation.mutate(question)}
                disabled={reproductionMutation.isPending}
              >
                {reproductionMutation.isPending
                  ? "Generating..."
                  : "Generate Reproduction Plan"}
              </Button>
            </div>
          )}

          {reproductionMutation.data && (
            <>
              <ReproductionResult result={reproductionMutation.data} />

              {!blueprintMutation.data && (
                <div className="rounded-xl border border-border bg-card p-8">
                  <h2 className="mb-3 text-lg font-semibold">
                    Implementation Blueprint
                  </h2>

                  <p className="mb-6 text-muted-foreground">
                    Generate exact file-level implementation instructions.
                  </p>

                  <Button
                    onClick={() => blueprintMutation.mutate(question)}
                    disabled={blueprintMutation.isPending}
                  >
                    {blueprintMutation.isPending
                      ? "Generating..."
                      : "Generate Blueprint"}
                  </Button>
                </div>
              )}
            </>
          )}

          {blueprintMutation.data && (
            <>
              <BlueprintResult result={blueprintMutation.data} />

              {!evaluationMutation.data && (
                <div className="rounded-xl border border-border bg-card p-8">
                  <h2 className="mb-3 text-lg font-semibold">
                    Blueprint Evaluation
                  </h2>

                  <p className="mb-6 text-muted-foreground">
                    Evaluate blueprint quality and implementation coverage.
                  </p>

                  <Button
                    onClick={() => evaluationMutation.mutate(question)}
                    disabled={evaluationMutation.isPending}
                  >
                    {evaluationMutation.isPending
                      ? "Evaluating..."
                      : "Evaluate Blueprint"}
                  </Button>
                </div>
              )}
            </>
          )}

          {evaluationMutation.data && (
            <EvaluationResult result={evaluationMutation.data} />
          )}
        </div>
      )}
    </PageContainer>
  );
}
