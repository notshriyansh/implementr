import { Paper } from "@/types/paper";

import { PaperRow } from "./paper-row";

interface Props {
  papers: Paper[];
  onIngest: (paper: Paper) => void;
  ingestingPaper?: string;
}

export function PaperTable({ papers, onIngest, ingestingPaper }: Props) {
  return (
    <div className="overflow-x-auto rounded-xl border border-border bg-card">
      <div className="grid grid-cols-12 px-6 py-4 border-b bg-muted/20 text-xs uppercase tracking-wider text-muted-foreground">
        <div className="col-span-7">Title</div>

        <div className="col-span-2">Tags</div>

        <div className="col-span-2">Status</div>

        <div className="col-span-1 text-right">Actions</div>
      </div>

      {papers.map((paper) => (
        <PaperRow
          key={paper.pdf_url}
          paper={paper}
          onIngest={() => onIngest(paper)}
          isLoading={ingestingPaper === paper.pdf_url}
        />
      ))}
    </div>
  );
}
