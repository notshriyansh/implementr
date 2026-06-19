import { Button } from "@/components/ui/button";

export function ResearchHeader() {
  return (
    <div className="flex items-start justify-between">
      <div>
        <div className="text-xs uppercase tracking-[0.25em] text-muted-foreground mb-4">
          01 · RESEARCH
        </div>

        <h1 className="text-5xl font-semibold tracking-tight">Paper library</h1>

        <p className="mt-4 text-muted-foreground max-w-2xl">
          Ingest arXiv preprints, read with grounded citations, and hand them to
          the workspace as implementation briefs.
        </p>
      </div>

      <Button className="rounded-xl">+ Ingest paper</Button>
    </div>
  );
}
