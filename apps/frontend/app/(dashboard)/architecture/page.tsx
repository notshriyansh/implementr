"use client";

import { ArchitectureQuery } from "@/components/architecture/architecture-query";
import { ArchitectureResult } from "@/components/architecture/architecture-result";
import { EmptyState } from "@/components/shared/empty-state";
import { PageContainer } from "@/components/shared/page-container";
import { ContextPanel } from "@/components/context/context-panel";

import { useArchitectureAnalysis } from "@/hooks/use-architecture-analysis";

export default function ArchitecturePage() {
  const mutation = useArchitectureAnalysis();

  return (
    <PageContainer>
      <section className="mb-8">
        <div className="text-xs uppercase tracking-[0.25em] text-muted-foreground mb-3">
          03 · ARCHITECTURE
        </div>

        <h1 className="text-3xl font-semibold tracking-tight lg:text-4xl">
          Architecture Explorer
        </h1>

        <p className="mt-4 max-w-3xl text-base leading-7 text-muted-foreground">
          Understand execution flow, dependencies, modification points, and
          overall system design before making implementation changes.
        </p>
      </section>

      <ContextPanel />

      <div className="mt-8">
        <ArchitectureQuery
          onAnalyze={(query) => mutation.mutate(query)}
          loading={mutation.isPending}
        />
      </div>

      {!mutation.data && (
        <div className="mt-10">
          <EmptyState
            title="Ready to inspect your architecture"
            description="Ask how a feature works, trace execution flow, identify modification points, or understand relationships between services and modules."
          />
        </div>
      )}

      {mutation.data && (
        <section className="mt-10">
          <ArchitectureResult result={mutation.data} />
        </section>
      )}
    </PageContainer>
  );
}
