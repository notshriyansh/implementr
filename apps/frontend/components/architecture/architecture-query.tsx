"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2 } from "lucide-react";

interface Props {
  onAnalyze: (query: string) => void;
  loading?: boolean;
}

export function ArchitectureQuery({ onAnalyze, loading }: Props) {
  const [query, setQuery] = useState("");

  return (
    <div className="rounded-lg border border-border bg-card p-6">
      <h2 className="font-semibold mb-4">Ask an Architecture Question</h2>

      <div className="flex gap-3">
        <Input
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="How does streaming work?"
          aria-label="Architecture question input"
        />

        <Button onClick={() => onAnalyze(query)} disabled={!query || loading} aria-label="Run architecture analysis">
          {loading ? (
            <>
              <Loader2 className="h-4 w-4 animate-spin" />
              Analyzing
            </>
          ) : (
            "Analyze"
          )}
        </Button>
      </div>
    </div>
  );
}
