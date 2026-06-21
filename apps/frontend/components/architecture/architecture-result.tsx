import { ArchitectureInsight } from "@/types/repository";

interface Props {
  result: ArchitectureInsight;
}

export function ArchitectureResult({ result }: Props) {
  return (
    <div className="space-y-6">
      <div className="border rounded-xl p-6">
        <h2 className="font-semibold mb-3">Summary</h2>

        <p>{result.summary}</p>
      </div>

      <div className="grid grid-cols-2 gap-6">
        <Section title="Relevant Files" items={result.relevant_files} />

        <Section title="Relevant Symbols" items={result.relevant_symbols} />

        <Section title="Execution Steps" items={result.execution_steps} />

        <Section
          title="Modification Points"
          items={result.modification_points}
        />
      </div>

      <div className="border rounded-xl p-6">
        <h2 className="font-semibold mb-3">Engineering Notes</h2>

        <ul className="space-y-2">
          {result.engineering_notes.map((note) => (
            <li key={note}>• {note}</li>
          ))}
        </ul>
      </div>

      <div className="border rounded-xl p-6">
        <h2 className="font-semibold mb-3">Reasoning</h2>

        <p>{result.reasoning}</p>
      </div>
    </div>
  );
}

function Section({ title, items }: { title: string; items: string[] }) {
  return (
    <div className="border rounded-xl p-6">
      <h3 className="font-semibold mb-3">{title}</h3>

      <ul className="space-y-2">
        {items.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </div>
  );
}
