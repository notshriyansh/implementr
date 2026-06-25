"use client";

import { ArchitectureQuery } from "@/components/architecture/architecture-query";
import { ArchitectureResult } from "@/components/architecture/architecture-result";
import { EmptyState } from "@/components/shared/empty-state";
import { PageContainer } from "@/components/shared/page-container";

import { useArchitectureAnalysis } from "@/hooks/use-architecture-analysis";

export default function ArchitecturePage() {
  const mutation = useArchitectureAnalysis();

  return (
    <PageContainer>
      <section className="mb-12">
        <div className="text-xs uppercase tracking-[0.25em] text-muted-foreground mb-4">
          03 · ARCHITECTURE
        </div>

        <h1 className="text-6xl font-semibold tracking-tighter">
          Architecture Explorer
        </h1>

        <p className="mt-5 max-w-3xl text-lg leading-8 text-muted-foreground">
          Understand execution flow, dependencies, modification points, and
          overall system design before making implementation changes.
        </p>
      </section>

      <ArchitectureQuery
        onAnalyze={(query) => mutation.mutate(query)}
        loading={mutation.isPending}
      />

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
