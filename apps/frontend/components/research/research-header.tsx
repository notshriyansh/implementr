import { Button } from "@/components/ui/button";

export function ResearchHeader() {
  return (
    <div className="flex flex-col gap-8 lg:flex-row lg:items-start lg:justify-between">
      <div className="max-w-4xl">
        <div className="mb-4 text-xs uppercase tracking-[0.25em] text-muted-foreground">
          01 · RESEARCH
        </div>

        <h1 className="text-4xl font-semibold leading-none tracking-tighter sm:text-5xl lg:text-6xl">
          Paper library
        </h1>

        <p className="mt-6 max-w-3xl text-base leading-7 text-muted-foreground lg:text-lg lg:leading-8">
          Ingest arXiv preprints, read with grounded citations, and hand them to
          the workspace as implementation briefs.
        </p>
      </div>

      <Button
        className="
          w-full
          rounded-xl
          sm:w-auto
          shrink-0
        "
      >
        + Ingest paper
      </Button>
    </div>
  );
}
