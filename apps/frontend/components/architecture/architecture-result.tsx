import { ArchitectureInsight } from "@/types/repository";
import { Badge } from "@/components/ui/badge";

interface Props {
  result: ArchitectureInsight;
}

export function ArchitectureResult({ result }: Props) {
  return (
    <div className="space-y-6">
      <div className="rounded-3xl border border-border/50 bg-card/40 p-8">
        <div className="mb-4 flex items-center justify-between">
          <h2 className="font-semibold">Summary</h2>

          <Badge>{Math.round(result.confidence * 100)}%</Badge>
        </div>

        <p className="leading-7 text-muted-foreground">{result.summary}</p>
      </div>

      <div className="grid gap-6 lg:grid-cols-2">
        <Section title="Relevant Files" items={result.relevant_files} />

        <Section title="Relevant Symbols" items={result.relevant_symbols} />
      </div>

      <Section title="Execution Flow" items={result.execution_steps} />

      <Section title="Modification Points" items={result.modification_points} />

      <Section title="Engineering Notes" items={result.engineering_notes} />

      <div className="rounded-3xl border border-border/50 bg-card/40 p-8">
        <h2 className="mb-4 font-semibold">Reasoning</h2>

        <p className="leading-7 text-muted-foreground">{result.reasoning}</p>
      </div>
    </div>
  );
}

function Section({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="rounded-3xl border border-border/50 bg-card/40 p-6">
      <h2 className="mb-4 font-semibold">{title}</h2>

      <ul className="space-y-3">
        {items.map((item) => (
          <li
            key={item}
            className="
              rounded-xl
              bg-muted/20
              px-3
              py-2
              text-sm
            "
          >
            {item}
          </li>
        ))}
      </ul>
    </div>
  );
}
