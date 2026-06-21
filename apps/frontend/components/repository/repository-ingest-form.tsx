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
    <div className="border rounded-xl p-6">
      <h2 className="font-semibold mb-4">Analyze Repository</h2>

      <div className="flex gap-3">
        <Input
          value={path}
          onChange={(e) => setPath(e.target.value)}
          placeholder="C:/Projects/implementr"
        />

        <Button onClick={() => onAnalyze(path)} disabled={loading || !path}>
          Analyze
        </Button>
      </div>
    </div>
  );
}
