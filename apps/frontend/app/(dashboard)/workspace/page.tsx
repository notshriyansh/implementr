"use client";

import { useHybridAnalysis } from "@/hooks/use-hybrid-analysis";

import { HybridQuery } from "@/components/workspace/hybrid-query";
import { HybridResult } from "@/components/workspace/hybrid-result";
import { Badge } from "@/components/ui/badge";
import { motion } from "framer-motion";

export default function WorkspacePage() {
  const mutation = useHybridAnalysis();

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
      className="max-w-350] mx-auto p-8"
    >
      <div className="mb-10">
        <div className="text-xs uppercase tracking-[0.25em] text-muted-foreground mb-4">
          04 · HYBRID
        </div>

        <h1 className="text-6xl font-semibold tracking-tighter">
          Implementation Workspace
        </h1>

        <p className="mt-4 text-muted-foreground max-w-3xl">
          Combine paper knowledge, repository intelligence, and architecture
          understanding to generate implementation guidance.
        </p>

        <div className="mb-8 flex gap-2 flex-wrap">
          <Badge variant="outline">Research</Badge>
          <Badge variant="outline">Repository</Badge>
          <Badge variant="outline">Architecture</Badge>
        </div>
      </div>

      <HybridQuery
        onAnalyze={(question) => mutation.mutate(question)}
        loading={mutation.isPending}
      />

      {mutation.data && (
        <div className="mt-8">
          <HybridResult result={mutation.data} />
        </div>
      )}
    </motion.div>
  );
}
