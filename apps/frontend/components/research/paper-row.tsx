"use client";

import { Paper } from "@/types/paper";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { useAppStore } from "@/stores/app-store";

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

  const recentPapers = useAppStore((state) => state.recentPapers);
  const isIngested = recentPapers.some((p) => p.pdf_url === paper.pdf_url);

  return (
    <div className="grid min-w-237.5 grid-cols-12 items-center border-b px-6 py-5 hover:bg-muted/20 hover:-translate-y-0.5 transition-all duration-300">
      <div className="col-span-7">
        <div className="space-y-2">
          <div className="flex items-center gap-2 text-xs text-muted-foreground">
            <span>arXiv</span>
            <span>•</span>
            <span>{new Date(paper.published).getFullYear()}</span>
          </div>

          <h3 className="font-medium text-[15px] leading-6">{paper.title}</h3>

          <p className="text-sm text-muted-foreground">{authors}</p>
        </div>
      </div>

      <div className="col-span-2 flex gap-2 flex-wrap">
        <Badge variant="outline">research</Badge>

        <Badge variant="outline">arxiv</Badge>
      </div>

      <div className="col-span-2">
        <PaperStatusBadge
          status={
            isLoading ? "INGESTING" : isIngested ? "INGESTED" : "NOT_INGESTED"
          }
        />
      </div>

      <div className="col-span-2 flex justify-end gap-2">
        <Button variant="ghost" size="sm" disabled>
          Open
        </Button>
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
