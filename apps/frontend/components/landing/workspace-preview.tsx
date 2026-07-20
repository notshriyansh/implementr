"use client";

import {
  CheckCircle2,
  ChevronRight,
  FileCode2,
  FolderTree,
  GitBranch,
  Sparkles,
} from "lucide-react";

import { FadeIn } from "@/components/shared/fade-in";

export function WorkspacePreview() {
  return (
    <section className="mx-auto max-w-7xl px-6 pb-28">
      <FadeIn>
        <div className="mb-8 flex items-end justify-between">
          <div>
            <div className="font-mono text-xs uppercase tracking-[0.28em] text-muted-foreground">
              Workspace Preview
            </div>

            <h2 className="mt-3 text-3xl font-medium tracking-tight">
              One workspace.
              <br />
              Every implementation step.
            </h2>
          </div>

          <div className="hidden text-sm text-muted-foreground lg:block">
            Paper → Repository → Blueprint
          </div>
        </div>

        <div className="overflow-hidden rounded-3xl border border-border bg-card">
          <div className="flex items-center justify-between border-b border-border px-6 py-4">
            <div className="flex items-center gap-2">
              <span className="h-2.5 w-2.5 rounded-full bg-muted-foreground/25" />
              <span className="h-2.5 w-2.5 rounded-full bg-muted-foreground/25" />
              <span className="h-2.5 w-2.5 rounded-full bg-muted-foreground/25" />
            </div>

            <span className="font-mono text-xs text-muted-foreground">
              IMPLEMENTR / WORKSPACE
            </span>
          </div>

          <div className="grid lg:grid-cols-[300px_1fr_320px]">
            <aside className="border-r border-border p-6">
              <div className="font-mono text-xs uppercase tracking-[0.24em] text-muted-foreground">
                Research
              </div>

              <h3 className="mt-4 text-xl font-medium">
                Llama 3: Open Foundation Models
              </h3>

              <p className="mt-3 text-sm leading-7 text-muted-foreground">
                Analyze architecture, implementation details and repository
                integration points.
              </p>

              <div className="mt-8 space-y-4">
                <div className="flex items-center gap-3 rounded-xl border border-border bg-background px-4 py-3">
                  <Sparkles className="h-4 w-4 text-muted-foreground" />

                  <span className="text-sm">Architecture reasoning</span>
                </div>

                <div className="flex items-center gap-3 rounded-xl border border-border bg-background px-4 py-3">
                  <GitBranch className="h-4 w-4 text-muted-foreground" />

                  <span className="text-sm">Repository implementation map</span>
                </div>
              </div>
            </aside>

            <main className="border-r border-border bg-[oklch(0.17_0.002_260)] p-6">
              <div className="mb-5 flex items-center gap-2 font-mono text-xs uppercase tracking-[0.24em] text-muted-foreground">
                <FolderTree className="h-3.5 w-3.5" />
                Repository
              </div>

              <div className="rounded-2xl border border-white/5 bg-[oklch(0.14_0.002_260)] p-5 font-mono text-[13px] leading-7">
                <div className="text-white/45">src</div>

                <div className="ml-4 text-white/70">
                  ├── models
                  <br />
                  │ ├── attention.py
                  <br />
                  │ ├── decoder.py
                  <br />
                  │ └── rotary.py
                  <br />
                  ├── inference
                  <br />
                  │ ├── generate.py
                  <br />
                  │ └── cache.py
                  <br />
                  └── serving
                </div>

                <div className="mt-5 rounded-lg border border-emerald-500/20 bg-emerald-500/8 px-4 py-3 text-emerald-300">
                  → Suggested modification:
                  <br />
                  models/attention.py
                </div>
              </div>
            </main>

            <aside className="p-6">
              <div className="font-mono text-xs uppercase tracking-[0.24em] text-muted-foreground">
                Blueprint
              </div>

              <div className="mt-6 space-y-5">
                {[
                  "Locate attention implementation",
                  "Compare algorithm with paper",
                  "Generate implementation plan",
                  "Validate affected execution flow",
                ].map((step) => (
                  <div
                    key={step}
                    className="flex items-start gap-3 rounded-xl border border-border bg-background px-4 py-4"
                  >
                    <CheckCircle2 className="mt-0.5 h-4 w-4 text-muted-foreground" />

                    <div className="flex-1">
                      <div className="text-sm font-medium">{step}</div>
                    </div>

                    <ChevronRight className="h-4 w-4 text-muted-foreground/40" />
                  </div>
                ))}

                <div className="rounded-xl border border-dashed border-border p-4">
                  <div className="flex items-center gap-2 text-sm font-medium">
                    <FileCode2 className="h-4 w-4" />
                    Implementation ready
                  </div>

                  <p className="mt-2 text-sm leading-6 text-muted-foreground">
                    Blueprint generated with repository-aware reasoning.
                  </p>
                </div>
              </div>
            </aside>
          </div>
        </div>
      </FadeIn>
    </section>
  );
}
