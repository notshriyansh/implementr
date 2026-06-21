"use client";

import { useState } from "react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";

import { useImplementationPlan } from "@/hooks/use-implementation-plan";

export function ImplementationPlan() {
  const [question, setQuestion] = useState("");

  const mutation = useImplementationPlan();

  async function handleGenerate() {
    if (!question.trim()) return;

    mutation.mutate(question);
  }

  return (
    <div className="space-y-6">
      <div className="border rounded-xl p-6">
        <h2 className="font-semibold mb-4">Generate Implementation Plan</h2>

        <Textarea
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="How can I implement Video Transformers in PyTorch?"
        />

        <Button
          className="mt-4"
          onClick={handleGenerate}
          disabled={mutation.isPending}
        >
          {mutation.isPending ? "Generating..." : "Generate Plan"}
        </Button>
      </div>

      {mutation.data && (
        <div className="border rounded-xl p-6">
          <div className="flex items-center justify-between mb-6">
            <h2 className="font-semibold">Implementation Plan</h2>

            <Button
              variant="outline"
              size="sm"
              onClick={() => navigator.clipboard.writeText(mutation.data.plan)}
            >
              Copy
            </Button>
          </div>

          <article className="prose prose-invert max-w-none">
            <ReactMarkdown remarkPlugins={[remarkGfm]}>
              {mutation.data.plan}
            </ReactMarkdown>
          </article>
        </div>
      )}
    </div>
  );
}
