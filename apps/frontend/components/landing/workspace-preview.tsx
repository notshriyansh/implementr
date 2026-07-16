export function WorkspacePreview() {
  return (
    <section className="mx-auto max-w-7xl px-6 pb-32">
      <div className="overflow-hidden rounded-3xl border border-border bg-card">
        <div className="border-b border-border px-6 py-4">
          <div className="text-xs uppercase tracking-[0.25em] text-muted-foreground">
            Workspace Preview
          </div>
        </div>

        <div className="grid lg:grid-cols-[320px_1fr_320px]">
          <div className="border-r border-border p-6">
            <div className="text-xs uppercase tracking-widest text-muted-foreground">
              Paper
            </div>

            <h3 className="mt-4 text-2xl font-semibold">FlashAttention-2</h3>

            <p className="mt-4 text-muted-foreground">
              Faster attention through better work partitioning and parallelism.
            </p>

            <div className="mt-6 rounded-xl bg-muted/20 p-4">
              Algorithm mapping
            </div>

            <div className="mt-4 rounded-xl bg-muted/20 p-4">
              Architecture gaps
            </div>
          </div>

          <div className="border-r border-border bg-black text-white p-6">
            <div className="mb-4 text-xs uppercase tracking-widest text-white/50">
              Repository Target
            </div>

            <pre className="font-mono text-sm leading-7 overflow-hidden">
              {`def flash_attn_forward(q, k, v):
    """
    FlashAttention-2 implementation
    """

    # implementation target

    return output`}
            </pre>
          </div>

          <div className="p-6">
            <div className="text-xs uppercase tracking-widest text-muted-foreground">
              Blueprint
            </div>

            <div className="mt-6 space-y-3">
              <div className="rounded-xl bg-muted/20 p-4">
                Modify flash_attn_forward
              </div>

              <div className="rounded-xl bg-muted/20 p-4">
                Add tiling strategy
              </div>

              <div className="rounded-xl bg-muted/20 p-4">
                Validate benchmark
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}
