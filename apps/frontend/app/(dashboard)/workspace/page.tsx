"use client";

import { useHybridAnalysis } from "@/hooks/use-hybrid-analysis";

import { HybridQuery } from "@/components/workspace/hybrid-query";
import { HybridResult } from "@/components/workspace/hybrid-result";

export default function WorkspacePage() {
  const mutation = useHybridAnalysis();

  return (
    <div className="max-w-7xl mx-auto p-8">
      <div className="mb-10">
        <div className="text-xs uppercase tracking-[0.25em] text-muted-foreground mb-4">
          04 · HYBRID
        </div>

        <h1 className="text-5xl font-semibold tracking-tight">
          Implementation Workspace
        </h1>

        <p className="mt-4 text-muted-foreground max-w-3xl">
          Combine paper knowledge, repository intelligence, and architecture
          understanding to generate implementation guidance.
        </p>
      </div>

      <HybridQuery
        onAnalyze={(question) => mutation.mutate(question)}
        loading={mutation.isPending}
      />

      {mutation.data && (
        <div className="mt-8">
          <HybridResult result={mutation.data.result} />
        </div>
      )}
    </div>
  );
}
