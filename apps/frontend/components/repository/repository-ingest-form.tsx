"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2 } from "lucide-react";

import { RepositorySource } from "@/types/repository";

interface Props {
  onAnalyze: (source: RepositorySource) => void;
  loading?: boolean;
}

export function RepositoryIngestForm({ onAnalyze, loading }: Props) {
  const [sourceType, setSourceType] = useState<"local" | "github">("local");
  const [value, setValue] = useState("");

  function handleAnalyze() {
    if (!value.trim()) {
      return;
    }

    if (sourceType === "local") {
      onAnalyze({
        type: "local",
        path: value,
      });
    } else {
      onAnalyze({
        type: "github",
        repository_url: value,
        branch: "main",
      });
    }
  }

  return (
    <div className="flex items-center gap-2">
      <select
        value={sourceType}
        onChange={(e) => setSourceType(e.target.value as "local" | "github")}
        className="h-9 rounded-md border bg-background px-3 text-sm"
      >
        <option value="local">Local</option>
        <option value="github">GitHub</option>
      </select>

      <Input
        value={value}
        onChange={(e) => setValue(e.target.value)}
        placeholder={
          sourceType === "local"
            ? "C:/Projects/implementr"
            : "https://github.com/openai/openai-python"
        }
        className="h-9 w-96 text-sm"
        aria-label="Repository source"
      />

      <Button
        size="sm"
        onClick={handleAnalyze}
        disabled={loading || !value.trim()}
        aria-label="Analyze repository"
      >
        {loading ? (
          <>
            <Loader2 className="mr-2 h-3.5 w-3.5 animate-spin" />
            Analyzing
          </>
        ) : (
          "Analyze"
        )}
      </Button>
    </div>
  );
}
