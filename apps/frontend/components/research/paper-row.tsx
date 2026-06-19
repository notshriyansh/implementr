"use client";

import { Paper } from "@/types/paper";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";

import { PaperStatusBadge } from "./paper-status-badge";

interface Props {
  paper: Paper;
  onIngest: () => void;
  isLoading?: boolean;
}

export function PaperRow({ paper, onIngest, isLoading }: Props) {
  const authors =
    paper.authors
      ?.slice(0, 3)
      .map((a) => a.name)
      .join(", ") || "Unknown";

  return (
    <div className="grid grid-cols-12 items-center border-b px-6 py-5 hover:bg-muted/30 transition-colors">
      <div className="col-span-7">
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span>arXiv</span>
            <span>•</span>
            <span>{new Date(paper.published).getFullYear()}</span>
          </div>

          <h3 className="font-semibold text-base">{paper.title}</h3>

          <p className="text-sm text-muted-foreground">{authors}</p>
        </div>
      </div>

      <div className="col-span-2 flex gap-2 flex-wrap">
        <Badge variant="outline">research</Badge>

        <Badge variant="outline">arxiv</Badge>
      </div>

      <div className="col-span-2">
        <PaperStatusBadge status={isLoading ? "INGESTING" : "NOT_INGESTED"} />
      </div>

      <div className="col-span-1 flex justify-end gap-2">
        <Button variant="ghost" size="sm" asChild>
          <a href={paper.pdf_url} target="_blank">
            View
          </a>
        </Button>

        <Button size="sm" onClick={onIngest} disabled={isLoading}>
          {isLoading ? "..." : "Ingest"}
        </Button>
      </div>
    </div>
  );
}
