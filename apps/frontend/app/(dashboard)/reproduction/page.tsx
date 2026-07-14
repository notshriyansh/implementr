"use client";

import { ContextPanel } from "@/components/context/context-panel";

import { EmptyState } from "@/components/shared/empty-state";
import { PageContainer } from "@/components/shared/page-container";

import { ReproductionQuery } from "@/components/reproduction/reproduction-query";
import { ReproductionResult } from "@/components/reproduction/reproduction-result";

import { useReproductionPlan } from "@/hooks/use-reproduction-plan";

export default function ReproductionPage() {
  const mutation = useReproductionPlan();

  return (
    <PageContainer>
      <section className="mb-12">
        <div className="mb-4 text-xs uppercase tracking-[0.25em] text-muted-foreground">
          05 · REPRODUCTION
        </div>

        <h1 className="text-4xl font-semibold tracking-tighter sm:text-5xl lg:text-6xl">
          Research Reproduction
        </h1>

        <p className="mt-5 max-w-3xl text-base leading-7 text-muted-foreground lg:text-lg lg:leading-8">
          Determine whether a research paper can be reproduced inside a
          repository and identify the missing concepts, architecture gaps and
          implementation targets.
        </p>
      </section>

      <ContextPanel />

      <div className="mt-8">
        <ReproductionQuery
          onAnalyze={(question) => mutation.mutate(question)}
          loading={mutation.isPending}
        />
      </div>

      {!mutation.data && (
        <div className="mt-10">
          <EmptyState
            title="Ready to generate a reproduction plan"
            description="Analyze a paper and repository to identify implementation gaps."
          />
        </div>
      )}

      {mutation.data && (
        <div className="mt-10">
          <ReproductionResult result={mutation.data} />
        </div>
      )}
    </PageContainer>
  );
}
