interface Props {
  imports: number;
  functions: number;
  classes: number;
}

export function FileMetrics({ imports, functions, classes }: Props) {
  return (
    <div className="grid grid-cols-3 gap-3">
      <MetricCard label="Imports" value={imports} />
      <MetricCard label="Functions" value={functions} />
      <MetricCard label="Classes" value={classes} />
    </div>
  );
}

function MetricCard({ label, value }: { label: string; value: number }) {
  return (
    <div
      className="
        rounded-lg
        border
        border-border
        bg-card
        p-4
      "
    >
      <div className="text-xs text-muted-foreground">{label}</div>

      <div className="mt-2 text-2xl font-semibold">{value}</div>
    </div>
  );
}
