"use client";

import { motion } from "framer-motion";

import { BlueprintEvaluationResult } from "@/types/repository";

interface Props {
  result: BlueprintEvaluationResult;
}

export function EvaluationResult({ result }: Props) {
  const overallPercent = Math.round(result.overall_score * 100);

  const strengths = [
    {
      label: "Gap Coverage",
      value: result.gap_coverage_score,
    },
    {
      label: "Implementation Coverage",
      value: result.implementation_score,
    },
    {
      label: "Risk Coverage",
      value: result.risk_score,
    },
  ].filter((item) => item.value >= 0.7);

  const weaknesses = [
    {
      label: "Target File Accuracy",
      value: result.target_file_score,
    },
    {
      label: "Target Symbol Accuracy",
      value: result.target_symbol_score,
    },
    {
      label: "Gap Coverage",
      value: result.gap_coverage_score,
    },
    {
      label: "Implementation Coverage",
      value: result.implementation_score,
    },
  ].filter((item) => item.value < 0.5);

  function getAssessment(score: number) {
    if (score >= 0.8) {
      return "Excellent blueprint quality.";
    }

    if (score >= 0.6) {
      return "Good blueprint quality.";
    }

    if (score >= 0.4) {
      return "Blueprint requires refinement.";
    }

    return "Blueprint quality is poor.";
  }

  return (
    <div className="space-y-8">
      <div className="rounded-xl border border-border bg-card p-8">
        <div className="flex items-center justify-between">
          <h2 className="font-semibold text-lg">Blueprint Evaluation</h2>

          <span className="font-mono text-3xl font-bold">
            {overallPercent}%
          </span>
        </div>

        <div className="mt-6 h-2 overflow-hidden rounded-full bg-muted">
          <motion.div
            initial={{ width: 0 }}
            animate={{
              width: `${overallPercent}%`,
            }}
            transition={{
              duration: 1,
            }}
            className="h-full rounded-full bg-foreground"
          />
        </div>

        <p className="mt-4 text-sm text-muted-foreground">
          {getAssessment(result.overall_score)}
        </p>
      </div>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-5">
        <MetricCard label="Target Files" value={result.target_file_score} />

        <MetricCard label="Target Symbols" value={result.target_symbol_score} />

        <MetricCard label="Gap Coverage" value={result.gap_coverage_score} />

        <MetricCard
          label="Implementation"
          value={result.implementation_score}
        />

        <MetricCard label="Risk Coverage" value={result.risk_score} />
      </div>

      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-xl border border-border bg-card p-6">
          <h2 className="mb-4 font-semibold text-green-500">Strengths</h2>

          <div className="space-y-3">
            {strengths.map((item) => (
              <div
                key={item.label}
                className="rounded-lg bg-muted/30 px-4 py-3 text-sm"
              >
                {item.label}
              </div>
            ))}
          </div>
        </div>

        <div className="rounded-xl border border-border bg-card p-6">
          <h2 className="mb-4 font-semibold text-amber-500">Weaknesses</h2>

          <div className="space-y-3">
            {weaknesses.map((item) => (
              <div
                key={item.label}
                className="rounded-lg bg-muted/30 px-4 py-3 text-sm"
              >
                ⚠ {item.label}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

function MetricCard({ label, value }: { label: string; value: number }) {
  const percent = Math.round(value * 100);

  return (
    <div className="rounded-xl border border-border bg-card p-5">
      <div className="text-sm text-muted-foreground">{label}</div>

      <div className="mt-3 text-3xl font-semibold">{percent}%</div>

      <div className="mt-4 h-1.5 rounded-full bg-muted">
        <div
          className="h-full rounded-full bg-foreground"
          style={{
            width: `${percent}%`,
          }}
        />
      </div>
    </div>
  );
}
