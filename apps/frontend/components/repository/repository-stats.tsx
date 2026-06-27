interface Props {
  label: string;
  value: number;
}

export function RepositoryStat({ label, value }: Props) {
  return (
    <div
      className="
        rounded-3xl
        border
        border-border/50
        bg-card/40
        p-6
      "
    >
      <div className="text-sm text-muted-foreground">{label}</div>

      <div className="mt-3 text-3xl font-semibold">{value}</div>
    </div>
  );
}
