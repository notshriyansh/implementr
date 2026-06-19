import { Badge } from "@/components/ui/badge";

interface Props {
  status: "NOT_INGESTED" | "INGESTING" | "INGESTED";
}

export function PaperStatusBadge({ status }: Props) {
  switch (status) {
    case "INGESTED":
      return (
        <Badge variant="outline" className="uppercase tracking-wider">
          Ingested
        </Badge>
      );

    case "INGESTING":
      return (
        <Badge variant="secondary" className="uppercase tracking-wider">
          Ingesting
        </Badge>
      );

    default:
      return (
        <Badge variant="outline" className="uppercase tracking-wider">
          Ready
        </Badge>
      );
  }
}
