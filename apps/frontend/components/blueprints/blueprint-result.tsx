import { Badge } from "@/components/ui/badge";

import { ImplementationBlueprint } from "@/types/repository";

interface Props {
  result: ImplementationBlueprint;
}

export function BlueprintResult({ result }: Props) {
  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-border bg-card p-8">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="font-semibold text-lg">Blueprint Summary</h2>

          <Badge variant="outline" className="font-mono bg-background">
            {Math.round(result.confidence * 100)}%
          </Badge>
        </div>

        <div className="mb-6 h-1.5 overflow-hidden rounded-full bg-muted">
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

      {result.blueprint_steps.map((step) => (
        <div
          key={`${step.file_path}-${step.symbol_name}`}
          className="rounded-xl border border-border bg-card p-8"
        >
          <div className="mb-6 flex flex-wrap gap-3">
            <Badge variant="outline">{step.change_type}</Badge>

            <Badge variant="outline" className="font-mono">
              {step.symbol_name}
            </Badge>
          </div>

          <h3 className="font-mono text-sm mb-4">{step.file_path}</h3>

          <p className="mb-6 text-muted-foreground">{step.reason}</p>

          <Section
            title="Implementation Steps"
            items={step.implementation_steps}
          />

          <Section title="Validation Steps" items={step.validation_steps} />

          <div className="mt-6 rounded-xl bg-muted/20 p-4">
            <h4 className="mb-2 text-sm font-medium">Expected Outcome</h4>

            <p className="text-sm text-muted-foreground">
              {step.expected_outcome}
            </p>
          </div>
        </div>
      ))}

      <Section title="Risks" items={result.risks} />
    </div>
  );
}

function Section({ title, items }: { title: string; items: string[] }) {
  if (!items.length) return null;

  return (
    <div className="mt-6">
      <h4 className="mb-3 font-medium">{title}</h4>

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
