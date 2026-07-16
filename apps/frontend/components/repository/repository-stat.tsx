interface Props {
  label: string;
  value: number | string;
  description?: string;
}

export function RepositoryStat({ label, value, description }: Props) {
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

      <div className="mt-1 text-xl font-semibold">{value}</div>

      {description && (
        <div className="mt-1 text-xs text-muted-foreground">{description}</div>
      )}
    </div>
  );
}
