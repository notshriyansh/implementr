"use client";

import { cn } from "@/lib/utils";

interface Props {
  hybridReady: boolean;
  reproductionReady: boolean;
  blueprintReady: boolean;
  evaluationReady: boolean;
}

export function WorkspacePipeline({
  hybridReady,
  reproductionReady,
  blueprintReady,
  evaluationReady,
}: Props) {
  const steps = [
    {
      label: "Hybrid",
      ready: hybridReady,
    },
    {
      label: "Reproduction",
      ready: reproductionReady,
    },
    {
      label: "Blueprint",
      ready: blueprintReady,
    },
    {
      label: "Evaluation",
      ready: evaluationReady,
    },
  ];

  return (
    <div className="rounded-lg border border-border bg-card p-6">
      <div className="flex items-center justify-between gap-4">
        {steps.map((step, index) => (
          <div key={step.label} className="flex flex-1 items-center">
            <div
              className={cn(
                "flex h-10 w-10 items-center justify-center rounded-full border text-sm font-semibold",
                step.ready
                  ? "border-green-500 bg-green-500/10 text-green-500"
                  : "border-border text-muted-foreground",
              )}
            >
              {index + 1}
            </div>

            <div className="ml-3">
              <div className="text-sm font-medium">{step.label}</div>
            </div>

            {index < steps.length - 1 && (
              <div className="mx-4 h-px flex-1 bg-border" />
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
