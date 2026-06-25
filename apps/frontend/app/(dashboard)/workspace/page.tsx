"use client";

import { useHybridAnalysis } from "@/hooks/use-hybrid-analysis";

import { HybridQuery } from "@/components/workspace/hybrid-query";
import { HybridResult } from "@/components/workspace/hybrid-result";
import { Badge } from "@/components/ui/badge";
import { motion } from "framer-motion";
import { EmptyState } from "@/components/shared/empty-state";
import { PageContainer } from "@/components/shared/page-container";

export default function WorkspacePage() {
  const mutation = useHybridAnalysis();

  return (
    <PageContainer>
      <div className="mb-10">
        <div className="text-xs uppercase tracking-[0.25em] text-muted-foreground mb-4">
          04 · HYBRID
        </div>

        <h1 className="text-6xl font-semibold tracking-tighter">
          Implementation Workspace
        </h1>

        <p className="mt-5 max-w-3xl text-lg leading-8 text-muted-foreground">
          Combine paper knowledge, repository intelligence, and architecture
          understanding to generate implementation guidance.
        </p>

        <div className="mt-6 flex gap-2 flex-wrap">
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
      </div>

      <HybridQuery
        onAnalyze={(question) => mutation.mutate(question)}
        loading={mutation.isPending}
      />

      {!mutation.data && (
        <EmptyState
          title="Ready for analysis"
          description="Ask a repository-aware implementation question to generate architecture-level implementation guidance."
        />
      )}
    </PageContainer>
  );
}
