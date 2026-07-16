import { HybridAnalysisResponse } from "@/types/repository";

import { Badge } from "@/components/ui/badge";
import { motion } from "framer-motion";

interface Props {
  result: HybridAnalysisResponse;
}

export function HybridResult({ result }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="space-y-8"
    >
      <div
        className="
          rounded-lg
          bg-card
          border
          border-border
          p-6
          "
      >
        <div className="mb-6 flex items-center justify-between">
          <h2 className="font-semibold text-lg">Implementation Summary</h2>
          <Badge variant="outline" className="font-mono bg-background">
            {Math.round(result.confidence * 100)}% Confident
          </Badge>
        </div>

        <div className="mb-6 h-1.5 overflow-hidden rounded-full bg-muted">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${Math.round(result.confidence * 100)}%` }}
            transition={{ duration: 1, delay: 0.2 }}
            className="h-full rounded-full bg-foreground"
          />
        </div>

        <p className="text-muted-foreground leading-relaxed">
          {result.summary}
        </p>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <Section title="Relevant Files" items={result.relevant_files} />

        <Section title="Relevant Symbols" items={result.relevant_symbols} />
      </div>

      <div className="rounded-lg border border-border bg-card p-6">
        <h2 className="font-semibold mb-6">Implementation Plan</h2>

        <div className="space-y-4">
          {result.implementation_steps.map((step, index) => (
            <div key={index} className="flex gap-4">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-muted text-xs font-semibold text-muted-foreground">
                {index + 1}
              </div>
              <div className="flex-1 rounded-lg bg-muted/30 px-4 py-3 text-sm leading-relaxed">
                {step}
              </div>
            </div>
          ))}
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <div className="rounded-lg border border-border bg-card p-6">
          <h2 className="font-semibold mb-5 text-amber-500/90">Identified Risks</h2>
          <ul className="space-y-3">
            {result.risks.map((risk) => (
              <li key={risk} className="flex gap-3 text-sm text-muted-foreground leading-relaxed">
                <span className="text-amber-500/50 mt-1">•</span>
                <span>{risk}</span>
              </li>
            ))}
          </ul>
        </div>

        <div className="rounded-lg border border-border bg-card p-6">
          <h2 className="font-semibold mb-5">Engineering Reasoning</h2>
          <p className="text-sm leading-relaxed text-muted-foreground">
            {result.reasoning}
          </p>
        </div>
      </div>
    </motion.div>
  );
}

function Section({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="rounded-lg border border-border bg-card p-6">
      <h2 className="mb-4 font-semibold">{title}</h2>

      <ul className="space-y-2">
        {items.map((item) => (
          <li
            key={item}
            className="rounded-lg bg-muted/20 px-3 py-2 font-mono text-sm"
          >
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}
