"use client";

import { Badge } from "@/components/ui/badge";

import { EmptyState } from "@/components/shared/empty-state";
import { PageContainer } from "@/components/shared/page-container";

import { HybridQuery } from "@/components/workspace/hybrid-query";
import { HybridResult } from "@/components/workspace/hybrid-result";

import { useHybridAnalysis } from "@/hooks/use-hybrid-analysis";
import { useAppStore } from "@/stores/app-store";

export default function WorkspacePage() {
  const mutation = useHybridAnalysis();

  const selectedPaper = useAppStore((state) => state.selectedPaper);

  const selectedRepository = useAppStore((state) => state.selectedRepository);

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

      {(selectedPaper || selectedRepository) && (
        <div className="mt-8 rounded-3xl border border-border/50 bg-card/40 p-6">
          <h3 className="mb-4 font-medium">Active Context</h3>

          <div className="space-y-2 text-sm">
            {selectedPaper && (
              <div>
                <span className="text-muted-foreground">Paper:</span>{" "}
                {selectedPaper.title}
              </div>
            )}

            {selectedRepository && (
              <div>
                <span className="text-muted-foreground">Repository:</span>{" "}
                {selectedRepository}
              </div>
            )}
          </div>
        </div>
      )}

      <HybridQuery
        onAnalyze={(question) => mutation.mutate(question)}
        loading={mutation.isPending}
      />

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
