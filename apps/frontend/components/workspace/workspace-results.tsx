"use client";

import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

import { HybridResult } from "./hybrid-result";

import { ReproductionResult } from "@/components/reproduction/reproduction-result";

import { BlueprintResult } from "@/components/blueprints/blueprint-result";

import { EvaluationResult } from "@/components/evaluation/evaluation-result";

interface Props {
  hybrid?: any;
  reproduction?: any;
  blueprint?: any;
  evaluation?: any;
}

export function WorkspaceResults({
  hybrid,
  reproduction,
  blueprint,
  evaluation,
}: Props) {
  return (
    <div className="rounded-xl border border-border bg-card p-8">
      <Tabs defaultValue="hybrid">
        <TabsList>
          <TabsTrigger value="hybrid">Hybrid</TabsTrigger>

          {reproduction && (
            <TabsTrigger value="reproduction">Reproduction</TabsTrigger>
          )}

          {blueprint && <TabsTrigger value="blueprint">Blueprint</TabsTrigger>}

          {evaluation && (
            <TabsTrigger value="evaluation">Evaluation</TabsTrigger>
          )}
        </TabsList>

        <TabsContent value="hybrid" className="mt-8">
          <HybridResult result={hybrid} />
        </TabsContent>

        {reproduction && (
          <TabsContent value="reproduction" className="mt-8">
            <ReproductionResult result={reproduction} />
          </TabsContent>
        )}

        {blueprint && (
          <TabsContent value="blueprint" className="mt-8">
            <BlueprintResult result={blueprint} />
          </TabsContent>
        )}

        {evaluation && (
          <TabsContent value="evaluation" className="mt-8">
            <EvaluationResult result={evaluation} />
          </TabsContent>
        )}
      </Tabs>
    </div>
  );
}
