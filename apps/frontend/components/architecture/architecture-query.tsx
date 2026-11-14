"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2 } from "lucide-react";

interface Props {
  onAnalyze: (query: string) => void;
  loading?: boolean;
  canAnalyze?: boolean;
}

export function ArchitectureQuery({
  onAnalyze,
  loading = false,
  canAnalyze = true,
}: Props) {
  const [query, setQuery] = useState("");

  function handleAnalyze() {
    const trimmedQuery = query.trim();

    if (!trimmedQuery || !canAnalyze || loading) {
      return;
    }

    onAnalyze(trimmedQuery);
  }

  return (
    <div className="rounded-lg border border-border bg-card p-6">
      <h2 className="mb-4 font-semibold">Ask an Architecture Question</h2>

      <div className="flex gap-3">
        <Input
          value={query}
          onChange={(event) => setQuery(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter") {
              handleAnalyze();
            }
          }}
          placeholder="How does document ingestion work?"
          aria-label="Architecture question input"
          disabled={!canAnalyze || loading}
        />

        <Button
          onClick={handleAnalyze}
          disabled={!query.trim() || loading || !canAnalyze}
          aria-label="Run architecture analysis"
        >
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

      {!canAnalyze && (
        <p className="mt-3 text-sm text-muted-foreground">
          Select and ingest a repository before analyzing its architecture.
        </p>
      )}
    </div>
  );
}
