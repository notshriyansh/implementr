"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

interface Props {
  onAnalyze: (repoPath: string) => void;
  loading?: boolean;
}

export function RepositoryIngestForm({ onAnalyze, loading }: Props) {
  const [path, setPath] = useState("");

  return (
    <div className="flex items-center gap-2">
      <Input
        value={path}
        onChange={(e) => setPath(e.target.value)}
        placeholder="C:/Projects/implementr"
        className="h-9 w-75 text-sm"
      />

      <Button
        size="sm"
        onClick={() => onAnalyze(path)}
        disabled={loading || !path}
      >
        Analyze
      </Button>
    </div>
  );
}
