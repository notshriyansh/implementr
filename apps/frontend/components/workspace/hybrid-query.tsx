"use client";

import { useState } from "react";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

import { useAppStore } from "@/stores/app-store";

interface Props {
  onAnalyze: (question: string) => void;
  loading?: boolean;
}

export function HybridQuery({ onAnalyze, loading }: Props) {
  const [question, setQuestion] = useState("");

  const addRecentQuestion = useAppStore((state) => state.addRecentQuestion);

  const setWorkspaceQuestion = useAppStore(
    (state) => state.setWorkspaceQuestion,
  );

  function handleSubmit() {
    if (!question) return;

    setWorkspaceQuestion(question);
    addRecentQuestion(question);
    onAnalyze(question);
  }

  return (
    <div className="rounded-xl border border-border bg-card p-8">
      <h2 className="font-semibold mb-4">Ask an Implementation Question</h2>

      <div className="flex gap-3">
        <Input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="How can I integrate Uniformer into this repository?"
        />

        <Button onClick={handleSubmit} disabled={!question || loading}>
          Analyze
        </Button>
      </div>
    </div>
  );
}
