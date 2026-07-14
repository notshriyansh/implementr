"use client";

import { useState } from "react";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface Props {
  onEvaluate: (question: string) => void;
  loading?: boolean;
}

export function EvaluationQuery({ onEvaluate, loading }: Props) {
  const [question, setQuestion] = useState("");

  function handleSubmit() {
    if (!question.trim()) return;

    onEvaluate(question);
  }

  return (
    <div className="rounded-xl border border-border bg-card p-8">
      <h2 className="mb-4 font-semibold">Evaluate Blueprint Quality</h2>

      <div className="flex gap-3">
        <Input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Can I reproduce RAG in this repository?"
        />

        <Button onClick={handleSubmit} disabled={!question || loading}>
          Evaluate
        </Button>
      </div>
    </div>
  );
}
