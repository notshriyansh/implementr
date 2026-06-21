"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface Props {
  onAnalyze: (query: string) => void;
  loading?: boolean;
}

export function ArchitectureQuery({ onAnalyze, loading }: Props) {
  const [query, setQuery] = useState("");

  return (
    <div className="border rounded-xl p-6">
      <h2 className="font-semibold mb-4">Ask an Architecture Question</h2>

      <div className="flex gap-3">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="How does streaming work?"
        />

        <Button onClick={() => onAnalyze(query)} disabled={!query || loading}>
          Analyze
        </Button>
      </div>
    </div>
  );
}
