"use client";

import { useAppStore } from "@/stores/app-store";

import { Badge } from "@/components/ui/badge";

import { uniquePapers } from "@/lib/paper-utils";

export function RecentPapersTable() {
  const recentPapers = uniquePapers(useAppStore((state) => state.recentPapers));

  if (recentPapers.length === 0) {
    return (
      <div className="rounded-xl border border-dashed p-10 text-center">
        <h3 className="font-medium">No papers ingested yet</h3>

        <p className="mt-2 text-sm text-muted-foreground">
          Search and ingest your first paper.
        </p>
      </div>
    );
  }

  return (
    <div className="rounded-xl overflow-hidden border">
      <div className="grid grid-cols-12 px-6 py-4 border-b text-xs uppercase tracking-wider text-muted-foreground">
        <div className="col-span-8">Title</div>

        <div className="col-span-2">Year</div>

        <div className="col-span-2">Status</div>
      </div>

      {recentPapers.map((paper) => (
        <div
          key={paper.pdf_url}
          className="grid grid-cols-12 items-center border-b px-6 py-5"
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
            <Badge>INGESTED</Badge>
          </div>
        </div>
      ))}
    </div>
  );
}
