interface Props {
  label: string;
  value: number | string;
  description?: string;
}

export function RepositoryStat({ label, value, description }: Props) {
  return (
    <div className="border-b border-border pb-5">
      <div className="font-mono text-[11px] uppercase tracking-[0.24em] text-muted-foreground">
        {label}
      </div>

      <div className="mt-3 text-3xl font-medium tracking-tight">{value}</div>

      {description && (
        <p className="mt-2 text-sm leading-6 text-muted-foreground">
          {description}
        </p>
      )}
    </div>
  );
}
