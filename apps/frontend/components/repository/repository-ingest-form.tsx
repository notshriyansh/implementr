"use client";

import { useState } from "react";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Loader2 } from "lucide-react";

interface Props {
  onAnalyze: (repoPath: string) => void;
  loading?: boolean;
}

export function RepositoryIngestForm({ onAnalyze, loading }: Props) {
  const [location, setLocation] = useState("");

  return (
    <div className="flex items-center gap-2">
      <Input
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        placeholder="Local path or GitHub URL"
        className="h-9 w-75 text-sm"
        aria-label="Repository path"
      />

      <Button
        size="sm"
        onClick={() => onAnalyze(location)}
        disabled={loading || !location}
        aria-label="Analyze repository"
      >
        {loading ? (
          <>
            <Loader2 className="h-3.5 w-3.5 animate-spin" />
            Analyzing
          </>
        ) : (
          "Analyze"
        )}
      </Button>
    </div>
  );
}
