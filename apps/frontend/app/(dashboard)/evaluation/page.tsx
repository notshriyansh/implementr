"use client";

import { ContextPanel } from "@/components/context/context-panel";

import { EmptyState } from "@/components/shared/empty-state";
import { PageContainer } from "@/components/shared/page-container";

import { EvaluationQuery } from "@/components/evaluation/evaluation-query";
import { EvaluationResult } from "@/components/evaluation/evaluation-result";

import { useBlueprintEvaluation } from "@/hooks/use-blueprint-evaluation";

export default function EvaluationPage() {
  const mutation = useBlueprintEvaluation();

  return (
    <PageContainer>
      <section className="mb-12">
        <div className="mb-4 text-xs uppercase tracking-[0.25em] text-muted-foreground">
          07 · EVALUATION
        </div>

        <h1 className="text-4xl font-semibold tracking-tighter sm:text-5xl lg:text-6xl">
          Blueprint Evaluation
        </h1>

        <p className="mt-5 max-w-3xl text-base leading-7 text-muted-foreground lg:text-lg lg:leading-8">
          Measure blueprint quality, coverage, implementation completeness and
          engineering confidence.
        </p>
      </section>

      <ContextPanel />

      <div className="mt-8">
        <EvaluationQuery
          onEvaluate={(question) => mutation.mutate(question)}
          loading={mutation.isPending}
        />
      </div>

      {!mutation.data && (
        <div className="mt-10">
          <EmptyState
            title="Ready to evaluate"
            description="Evaluate generated implementation blueprints and inspect engineering quality metrics."
          />
        </div>
      )}

      {mutation.data && (
        <div className="mt-10">
          <EvaluationResult result={mutation.data} />
        </div>
      )}
    </PageContainer>
  );
}
