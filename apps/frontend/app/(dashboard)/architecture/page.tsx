"use client";

import { ArchitectureQuery } from "@/components/architecture/architecture-query";
import { ArchitectureResult } from "@/components/architecture/architecture-result";

import { useArchitectureAnalysis } from "@/hooks/use-architecture-analysis";

export default function ArchitecturePage() {
  const mutation = useArchitectureAnalysis();

  return (
    <div className="max-w-7xl mx-auto p-8">
      <div className="mb-10">
        <div className="text-xs uppercase tracking-[0.25em] text-muted-foreground mb-4">
          03 · ARCHITECTURE
        </div>

        <h1 className="text-5xl font-semibold tracking-tight">
          Architecture Explorer
        </h1>

        <p className="mt-4 text-muted-foreground max-w-2xl">
          Understand execution flow, dependencies, modification points, and
          system design.
        </p>
      </div>

      <ArchitectureQuery
        onAnalyze={(query) => mutation.mutate(query)}
        loading={mutation.isPending}
      />

      {mutation.data && (
        <div className="mt-8">
          <ArchitectureResult result={mutation.data} />
        </div>
      )}
    </div>
  );
}
