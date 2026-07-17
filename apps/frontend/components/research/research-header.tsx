export function ResearchHeader() {
  return (
    <div className="flex flex-col gap-6 lg:flex-row lg:items-start lg:justify-between">
      <div className="max-w-4xl">
        <div className="mb-3 text-xs uppercase tracking-[0.25em] text-muted-foreground">
          01 · RESEARCH
        </div>

        <h1 className="text-3xl font-semibold tracking-tight lg:text-4xl">
          Paper library
        </h1>

        <p className="mt-4 max-w-3xl text-base leading-7 text-muted-foreground">
          Ingest arXiv preprints, read with grounded citations, and hand them to
          the workspace as implementation briefs.
        </p>
      </div>
    </div>
  );
}
