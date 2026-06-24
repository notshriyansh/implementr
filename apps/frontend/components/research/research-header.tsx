import { Button } from "@/components/ui/button";

export function ResearchHeader() {
  return (
    <div className="flex items-start justify-between">
      <div>
        <div className="text-xs uppercase tracking-[0.25em] text-muted-foreground mb-4">
          01 · RESEARCH
        </div>

        <h1 className="text-6xl font-semibold tracking-[-0.04em] leading-none">
          Paper library
        </h1>

        <p className="mt-6 text-lg text-muted-foreground max-w-3xl leading-8">
          Ingest arXiv preprints, read with grounded citations, and hand them to
          the workspace as implementation briefs.
        </p>
      </div>

      <Button className="rounded-xl">+ Ingest paper</Button>
    </div>
  );
}
