"use client";

import Link from "next/link";

import { Button } from "@/components/ui/button";

export function LandingHero() {
  return (
    <section className="mx-auto max-w-7xl px-6 pt-24 pb-24">
      <div className="max-w-4xl">
        <div className="mb-6 inline-flex items-center rounded-full border px-4 py-1 text-xs uppercase tracking-[0.25em] text-muted-foreground">
          Research → Repository → Implementation
        </div>

        <h1 className="max-w-5xl text-6xl font-semibold tracking-tighter lg:text-8xl">
          Architecture-aware implementation for ML engineers.
        </h1>

        <p className="mt-8 max-w-3xl text-xl leading-9 text-muted-foreground">
          Move from research papers to production repositories with structured
          reasoning. Analyze symbols, trace execution flows, and generate
          implementation blueprints grounded in real codebases.
        </p>

        <div className="mt-10 flex gap-4">
          <Button asChild size="lg">
            <Link href="/research">Enter Workspace</Link>
          </Button>

          <Button asChild variant="outline" size="lg">
            <Link href="/workspace">See Workspace</Link>
          </Button>
        </div>
      </div>
    </section>
  );
}
