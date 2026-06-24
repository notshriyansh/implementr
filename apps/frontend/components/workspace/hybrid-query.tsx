"use client";

import { useState } from "react";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface Props {
  onAnalyze: (question: string) => void;
  loading?: boolean;
}

export function HybridQuery({ onAnalyze, loading }: Props) {
  const [question, setQuestion] = useState("");

  return (
    <div className="rounded-3xl border border-border/50 bg-card/50 backdrop-blur-sm p-8">
      <h2 className="font-semibold mb-4">Ask an Implementation Question</h2>

      <div className="flex gap-3">
        <Input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="How can I integrate Uniformer into this repository?"
        />

        <Button
          onClick={() => onAnalyze(question)}
          disabled={!question || loading}
        >
          Analyze
        </Button>
      </div>
    </div>
  );
}
