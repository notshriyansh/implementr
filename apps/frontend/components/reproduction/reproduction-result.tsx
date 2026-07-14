"use client";

import { Badge } from "@/components/ui/badge";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import { ResearchReproductionPlan } from "@/types/repository";

interface Props {
  result: ResearchReproductionPlan;
}

export function ReproductionResult({ result }: Props) {
  return (
    <div className="space-y-6">
      <div className="rounded-xl border border-border bg-card p-8">
        <div className="mb-6 flex items-center justify-between">
          <h2 className="font-semibold text-lg">Reproduction Summary</h2>

          <Badge variant="outline" className="font-mono bg-background">
            {Math.round(result.confidence * 100)}% Confident
          </Badge>
        </div>

        <div className="mb-6 h-1.5 overflow-hidden rounded-full bg-muted">
          <div
            className="h-full bg-foreground transition-all duration-1000"
            style={{
              width: `${Math.round(result.confidence * 100)}%`,
            }}
          />
        </div>

        <p className="leading-7 text-muted-foreground">
          {result.paper_summary}
        </p>
      </div>

      <div className="rounded-xl border border-border bg-card p-8">
        <Tabs defaultValue="concepts">
          <TabsList>
            <TabsTrigger value="concepts">Concept Analysis</TabsTrigger>

            <TabsTrigger value="repository">Repository Impact</TabsTrigger>

            <TabsTrigger value="implementation">
              Implementation Plan
            </TabsTrigger>

            <TabsTrigger value="outcomes">Outcome Analysis</TabsTrigger>
          </TabsList>

          <TabsContent value="concepts" className="mt-8">
            <div className="grid gap-6 lg:grid-cols-2">
              <Section
                title="Concept Mappings"
                items={result.concept_mappings}
              />

              <Section
                title="Architecture Gaps"
                items={result.architecture_gaps}
              />
            </div>
          </TabsContent>

          <TabsContent value="repository" className="mt-8">
            <div className="grid gap-6 lg:grid-cols-2">
              <Section
                title="Repository Targets"
                items={result.repository_targets}
              />

              <Section
                title="Modification Targets"
                items={result.modification_targets}
              />
            </div>
          </TabsContent>

          <TabsContent value="implementation" className="mt-8">
            <div className="grid gap-6 lg:grid-cols-2">
              <Section
                title="Implementation Steps"
                items={result.implementation_steps}
              />

              <Section
                title="Required Changes"
                items={result.required_changes}
              />

              <Section
                title="Training Changes"
                items={result.training_changes}
              />

              <Section
                title="Evaluation Changes"
                items={result.evaluation_changes}
              />
            </div>
          </TabsContent>

          <TabsContent value="outcomes" className="mt-8">
            <div className="grid gap-6 lg:grid-cols-2">
              <Section title="Benchmark Tasks" items={result.benchmark_tasks} />

              <Section
                title="Success Criteria"
                items={result.success_criteria}
              />

              <Section title="Risks" items={result.risks} />
            </div>
          </TabsContent>
        </Tabs>
      </div>
    </div>
  );
}

function Section({ title, items }: { title: string; items: string[] }) {
  if (!items?.length) return null;

  return (
    <div className="rounded-xl border border-border bg-background p-6">
      <h3 className="mb-4 font-semibold">{title}</h3>

      <div className="space-y-3">
        {items.map((item) => (
          <div
            key={item}
            className="
              rounded-xl
              bg-muted/30
              px-4
              py-3
              text-sm
              leading-relaxed
            "
          >
            {item}
          </div>
        ))}
      </div>
    </div>
  );
}
