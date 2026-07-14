"use client";

import { ContextPanel } from "@/components/context/context-panel";

import { EmptyState } from "@/components/shared/empty-state";
import { PageContainer } from "@/components/shared/page-container";

import { BlueprintQuery } from "@/components/blueprints/blueprint-query";
import { BlueprintResult } from "@/components/blueprints/blueprint-result";

import { useBlueprint } from "@/hooks/use-blueprint";

export default function BlueprintsPage() {
  const mutation = useBlueprint();

  return (
    <PageContainer>
      <section className="mb-12">
        <div className="mb-4 text-xs uppercase tracking-[0.25em] text-muted-foreground">
          06 · BLUEPRINTS
        </div>

        <h1 className="text-4xl font-semibold tracking-tighter sm:text-5xl lg:text-6xl">
          Implementation Blueprint
        </h1>

        <p className="mt-5 max-w-3xl text-base leading-7 text-muted-foreground lg:text-lg lg:leading-8">
          Generate exact implementation targets, symbols, validation steps and
          expected outcomes for reproducing research ideas inside real
          repositories.
        </p>
      </section>

      <ContextPanel />

      <div className="mt-8">
        <BlueprintQuery
          onGenerate={(question) => mutation.mutate(question)}
          loading={mutation.isPending}
        />
      </div>

      {!mutation.data && (
        <div className="mt-10">
          <EmptyState
            title="Ready to generate a blueprint"
            description="Create an implementation blueprint from research and repository context."
          />
        </div>
      )}

      {mutation.data && (
        <div className="mt-10">
          <BlueprintResult result={mutation.data} />
        </div>
      )}
    </PageContainer>
  );
}
