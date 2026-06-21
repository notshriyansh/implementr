interface Props {
  onSelect: (prompt: string) => void;
}

const templates = [
  "Implement this paper in PyTorch",
  "Implement this paper in FastAPI",
  "Adapt this paper into an existing codebase",
  "Convert this research into production architecture",
];

export function PlanTemplates({ onSelect }: Props) {
  return (
    <div className="grid grid-cols-2 gap-3 mb-6">
      {templates.map((template) => (
        <button
          key={template}
          onClick={() => onSelect(template)}
          className="text-left border rounded-xl p-4 hover:bg-muted/30 transition"
        >
          {template}
        </button>
      ))}
    </div>
  );
}
