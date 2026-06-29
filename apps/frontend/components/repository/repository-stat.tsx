interface Props {
  label: string;
  value: number | string;
  description?: string;
}

export function RepositoryStat({ label, value, description }: Props) {
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

      <div className="mt-2 text-3xl font-semibold">{value}</div>

      {description && (
        <div className="mt-2 text-xs text-muted-foreground">{description}</div>
      )}
    </div>
  );
}
