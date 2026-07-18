"use client";

import { FileCode, Layers, CheckCircle2 } from "lucide-react";

import { FadeIn } from "@/components/shared/fade-in";

export function WorkspacePreview() {
  return (
    <section className="mx-auto max-w-7xl px-6 pb-24 sm:pb-32">
      <FadeIn>
        <div className="overflow-hidden rounded-2xl border border-border bg-card shadow-sm sm:rounded-3xl">
          <div className="border-b border-border px-5 py-3.5 sm:px-6 sm:py-4">
            <div className="text-xs uppercase tracking-[0.25em] text-muted-foreground">
              Workspace Preview
            </div>
          </div>

          <div className="grid lg:grid-cols-[300px_1fr_300px] xl:grid-cols-[320px_1fr_320px]">
            {/* Paper panel */}
            <div className="border-b border-border p-5 sm:p-6 lg:border-b-0 lg:border-r">
              <div className="text-[11px] uppercase tracking-widest text-muted-foreground">
                Paper
              </div>

              <h3 className="mt-4 text-xl font-semibold sm:text-2xl">
                FlashAttention-2
              </h3>

              <p className="mt-3 text-sm leading-relaxed text-muted-foreground sm:mt-4">
                Faster attention through better work partitioning and
                parallelism.
              </p>

              <div className="mt-5 space-y-2.5 sm:mt-6 sm:space-y-3">
                <div className="flex items-center gap-3 rounded-lg border border-border/60 bg-muted/10 px-4 py-3 text-sm">
                  <Layers className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
                  <span>Algorithm mapping</span>
                </div>

                <div className="flex items-center gap-3 rounded-lg border border-border/60 bg-muted/10 px-4 py-3 text-sm">
                  <Layers className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
                  <span>Architecture gaps</span>
                </div>
              </div>
            </div>

            <div className="border-b border-border bg-[oklch(0.1_0_0)] p-5 sm:p-6 lg:border-b-0 lg:border-r">
              <div className="mb-4 text-[11px] uppercase tracking-widest text-white/40">
                Repository Target
              </div>

              <div className="overflow-hidden rounded-lg">
                <pre className="font-mono text-[13px] leading-7 text-white/80">
                  <code>{`def flash_attn_forward(q, k, v):
    """
    FlashAttention-2 implementation
    """

    # implementation target

    return output`}</code>
                </pre>
              </div>
            </div>

            <div className="p-5 sm:p-6">
              <div className="text-[11px] uppercase tracking-widest text-muted-foreground">
                Blueprint
              </div>

              <div className="mt-5 space-y-2.5 sm:mt-6 sm:space-y-3">
                <div className="flex items-center gap-3 rounded-lg border border-border/60 bg-muted/10 px-4 py-3 text-sm">
                  <FileCode className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
                  <span>Modify flash_attn_forward</span>
                </div>

                <div className="flex items-center gap-3 rounded-lg border border-border/60 bg-muted/10 px-4 py-3 text-sm">
                  <Layers className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
                  <span>Add tiling strategy</span>
                </div>

                <div className="flex items-center gap-3 rounded-lg border border-border/60 bg-muted/10 px-4 py-3 text-sm">
                  <CheckCircle2 className="h-3.5 w-3.5 shrink-0 text-muted-foreground" />
                  <span>Validate benchmark</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </FadeIn>
    </section>
  );
}
