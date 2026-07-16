"use client";

import { useAppStore } from "@/stores/app-store";

import { uniquePapers } from "@/lib/paper-utils";
import { PaperStatusBadge } from "./paper-status-badge";

export function RecentPapersTable() {
  const recentPapers = uniquePapers(useAppStore((state) => state.recentPapers));

  if (recentPapers.length === 0) {
    return (
      <div className="rounded-lg border border-dashed border-border p-10 text-center">
        <h3 className="font-medium">No papers ingested yet</h3>

        <p className="mt-2 text-sm text-muted-foreground">
          Search and ingest your first paper.
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-lg overflow-hidden border border-border bg-card">
      <div className="grid grid-cols-12 px-6 py-3 border-b border-border bg-muted/10 text-xs uppercase tracking-wider text-muted-foreground">
        <div className="col-span-8">Title</div>

        <div className="col-span-2">Year</div>

        <div className="col-span-2">Status</div>
      </div>

      {recentPapers.map((paper) => (
        <div
          key={paper.pdf_url}
          className="grid grid-cols-12 items-center border-b border-border px-6 py-4 hover:bg-muted/50 transition-colors"
        >
          <div className="col-span-8">
            <div className="font-medium">{paper.title}</div>

            <div className="mt-1 text-sm text-muted-foreground">
              {paper.authors
                ?.slice(0, 3)
                .map((a) => a.name)
                .join(", ")}
            </div>
          </div>

          <div className="col-span-2 text-sm text-muted-foreground">
            {new Date(paper.published).getFullYear()}
          </div>

          <div className="col-span-2">
            <PaperStatusBadge status="INGESTED" />
          </div>
        </div>
      ))}
    </div>
  );
}
