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
          rounded-3xl
          bg-card/40
          border
          border-border/50
          p-8
          "
      >
        <h2 className="font-semibold mb-3">Implementation Summary</h2>

        <p className="text-muted-foreground">{result.summary}</p>
      </div>

      <div
        className="
          rounded-3xl
          bg-muted/20
          p-6
          "
      >
        <div className="flex items-center justify-between">
          <span className="font-medium">Confidence</span>

          <Badge>{Math.round(result.confidence * 100)}%</Badge>
        </div>
      </div>

      <div className="grid md:grid-cols-2 gap-6">
        <Section title="Relevant Files" items={result.relevant_files} />

        <Section title="Relevant Symbols" items={result.relevant_symbols} />
      </div>

      <div className="border rounded-xl p-6">
        <h2 className="font-semibold mb-4">Implementation Steps</h2>

        <ol className="space-y-3">
          {result.implementation_steps.map((step, index) => (
            <li key={index} className="flex gap-3">
              <span className="font-mono text-muted-foreground">
                {index + 1}.
              </span>

              <span>{step}</span>
            </li>
          ))}
        </ol>
      </div>

      <div className="border rounded-xl p-6">
        <h2 className="font-semibold mb-4">Risks</h2>

        <ul className="space-y-2">
          {result.risks.map((risk) => (
            <li key={risk} className="text-muted-foreground">
              • {risk}
            </li>
          ))}
        </ul>
      </div>

      <div className="border rounded-xl p-6">
        <h2 className="font-semibold mb-4">Engineering Reasoning</h2>

        <p className="leading-7 text-muted-foreground">{result.reasoning}</p>
      </div>
    </motion.div>
  );
}

function Section({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="border rounded-xl p-6">
      <h2 className="font-semibold mb-4">{title}</h2>

      <ul className="space-y-2">
        {items.map((item) => (
          <li key={item} className="font-mono text-sm">
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}
