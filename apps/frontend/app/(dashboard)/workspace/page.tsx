"use client";

import { Badge } from "@/components/ui/badge";

import { EmptyState } from "@/components/shared/empty-state";
import { PageContainer } from "@/components/shared/page-container";

import { HybridQuery } from "@/components/workspace/hybrid-query";
import { HybridResult } from "@/components/workspace/hybrid-result";

import { useHybridAnalysis } from "@/hooks/use-hybrid-analysis";
import { ContextPanel } from "@/components/context/context-panel";

export default function WorkspacePage() {
  const mutation = useHybridAnalysis();

  return (
    <PageContainer>
      <section className="mb-12">
        <div className="mb-4 text-xs uppercase tracking-[0.25em] text-muted-foreground">
          04 · HYBRID
        </div>

        <h1 className="text-4xl font-semibold tracking-tighter sm:text-5xl lg:text-6xl">
          Implementation Workspace
        </h1>

        <p className="mt-5 max-w-3xl text-base leading-7 text-muted-foreground lg:text-lg lg:leading-8">
          Combine paper knowledge, repository intelligence and architecture
          understanding to generate implementation guidance.
        </p>

        <div className="mt-6 flex flex-wrap gap-2">
          <Badge variant="secondary" className="rounded-full px-3">
            Research
          </Badge>

          <Badge variant="secondary" className="rounded-full px-3">
            Repository
          </Badge>

          <Badge variant="secondary" className="rounded-full px-3">
            Architecture
          </Badge>
        </div>
      </section>

      <div className="mt-8">
        <ContextPanel />
      </div>

      <div className="mt-8">
        <HybridQuery
          onAnalyze={(question) => mutation.mutate(question)}
          loading={mutation.isPending}
        />
      </div>

      {!mutation.data && (
        <div className="mt-10">
          <EmptyState
            title="Ready for analysis"
            description="Ask a repository-aware implementation question to generate implementation guidance."
          />
        </div>
      )}

      {mutation.data && (
        <div className="mt-10">
          <HybridResult result={mutation.data} />
        </div>
      )}
    </PageContainer>
  );
}
