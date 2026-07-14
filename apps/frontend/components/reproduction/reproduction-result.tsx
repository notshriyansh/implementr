import { Badge } from "@/components/ui/badge";

import { ResearchReproductionPlan } from "@/types/repository";

interface Props {
  result: ResearchReproductionPlan;
}

export function ReproductionResult({ result }: Props) {
  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-border bg-card p-8">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="font-semibold text-lg">Reproduction Summary</h2>

          <Badge variant="outline" className="font-mono bg-background">
            {Math.round(result.confidence * 100)}% Confident
          </Badge>
        </div>

        <div className="mb-6 h-1.5 rounded-full bg-muted overflow-hidden">
          <div
            className="h-full bg-foreground transition-all duration-1000"
            style={{
              width: `${Math.round(result.confidence * 100)}%`,
            }}
          />
        </div>

        <p className="leading-7 text-muted-foreground">
          {result.paper_summary}
        </p>
      </div>

      <Section title="Concept Mappings" items={result.concept_mappings} />

      <Section title="Architecture Gaps" items={result.architecture_gaps} />

      <Section title="Repository Targets" items={result.repository_targets} />

      <Section
        title="Modification Targets"
        items={result.modification_targets}
      />

      <Section
        title="Implementation Steps"
        items={result.implementation_steps}
      />

      <Section title="Required Changes" items={result.required_changes} />

      <Section title="Training Changes" items={result.training_changes} />

      <Section title="Evaluation Changes" items={result.evaluation_changes} />

      <Section title="Benchmark Tasks" items={result.benchmark_tasks} />

      <Section title="Success Criteria" items={result.success_criteria} />

      <Section title="Risks" items={result.risks} />
    </div>
  );
}

function Section({ title, items }: { title: string; items: string[] }) {
  if (!items.length) return null;

  return (
    <div className="rounded-xl border border-border bg-card p-6">
      <h2 className="mb-4 font-semibold">{title}</h2>

      <div className="space-y-3">
        {items.map((item) => (
          <div key={item} className="rounded-xl bg-muted/20 px-4 py-3 text-sm">
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}
