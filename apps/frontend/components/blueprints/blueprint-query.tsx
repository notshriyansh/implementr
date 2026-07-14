"use client";

import { useState } from "react";

import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";

interface Props {
  onGenerate: (question: string) => void;
  loading?: boolean;
}

export function BlueprintQuery({ onGenerate, loading }: Props) {
  const [question, setQuestion] = useState("");

  return (
    <div className="rounded-xl border border-border bg-card p-8">
      <h2 className="mb-4 font-semibold">Generate Implementation Blueprint</h2>

      <div className="flex gap-3">
        <Input
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Implement RAG inside this repository"
        />

        <Button
          disabled={!question || loading}
          onClick={() => onGenerate(question)}
        >
          Generate
        </Button>
      </div>
    </div>
  );
}
