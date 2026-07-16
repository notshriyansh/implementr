import { Badge } from "@/components/ui/badge";

interface Props {
  status: "NOT_INGESTED" | "INGESTING" | "INGESTED";
}

const statusConfig = {
  INGESTED: {
    label: "Ingested",
    className: "border-green-500/30 text-green-500 bg-green-500/10",
  },
  INGESTING: {
    label: "Ingesting",
    className: "border-amber-500/30 text-amber-500 bg-amber-500/10",
  },
  NOT_INGESTED: {
    label: "Ready",
    className: "border-border text-muted-foreground",
  },
} as const;

export function PaperStatusBadge({ status }: Props) {
  const config = statusConfig[status];

  return (
    <Badge
      variant="outline"
      className={`uppercase tracking-wider ${config.className}`}
    >
      {config.label}
    </Badge>
  );
}
