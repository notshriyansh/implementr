import { ArchitectureInsight } from "@/types/repository";
import { Badge } from "@/components/ui/badge";

interface Props {
  result: ArchitectureInsight;
}

export function ArchitectureResult({ result }: Props) {
  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-border bg-card p-8">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="font-semibold text-lg">Architecture Summary</h2>
          <Badge variant="outline" className="font-mono bg-background">
            {Math.round(result.confidence * 100)}% Confident
          </Badge>
        </div>

        <div className="mb-6 h-1.5 overflow-hidden rounded-full bg-muted">
          <div
            className="h-full rounded-full bg-foreground transition-all duration-1000 ease-out"
            style={{ width: `${Math.round(result.confidence * 100)}%` }}
          />
        </div>

        <p className="leading-7 text-muted-foreground">{result.summary}</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <CardSection
          title="Relevant Files"
          items={result.relevant_files}
          monospace
        />

        <CardSection title="Relevant Symbols" items={result.relevant_symbols} />
      </div>

      <ExecutionTimeline steps={result.execution_steps} />

      <CardSection
        title="Modification Points"
        items={result.modification_points}
      />

      <CardSection title="Engineering Notes" items={result.engineering_notes} />

      <div className="rounded-xl border border-border bg-card p-8">
        <h2 className="mb-4 font-semibold">Engineering Reasoning</h2>

        <p className="leading-7 text-muted-foreground">{result.reasoning}</p>
      </div>
    </div>
  );
}

function CardSection({
  title,
  items,
  monospace = false,
}: {
  title: string;
  items: string[];
  monospace?: boolean;
}) {
  return (
    <div className="rounded-xl border border-border bg-card p-6">
      <h2 className="mb-4 font-semibold">{title}</h2>

      <div className="space-y-3">
        {items.map((item) => (
          <div
            key={item}
            className={`
              rounded-xl
              bg-muted/20
              px-4
              py-3
              text-sm
              ${monospace ? "font-mono" : ""}
            `}
          >
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}

function ExecutionTimeline({ steps }: { steps: string[] }) {
  return (
    <div className="rounded-xl border border-border bg-card p-6">
      <h2 className="mb-6 font-semibold">Execution Flow</h2>

      <div className="space-y-4">
        {steps.map((step, index) => (
          <div key={step} className="flex gap-4">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-muted text-xs font-semibold text-muted-foreground">
              {index + 1}
            </div>

            <div className="flex-1 rounded-xl bg-muted/30 px-5 py-4 text-sm leading-relaxed">
              {step}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
