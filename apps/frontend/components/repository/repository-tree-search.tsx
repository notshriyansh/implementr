"use client";

import { Search } from "lucide-react";

interface Props {
  value: string;
  onChange: (value: string) => void;
}

export function RepositoryTreeSearch({ value, onChange }: Props) {
  return (
    <div className="border-b border-border/50 p-3">
      <div className="relative">
        <Search className="absolute left-3 top-3 h-4 w-4 text-muted-foreground" />

        <input
          value={value}
          onChange={(e) => onChange(e.target.value)}
          placeholder="Search files..."
          className="
            h-10
            w-full
            rounded-xl
            border
            border-border/50
            bg-background
            pl-9
            pr-3
            text-sm
            outline-none
          "
        />
      </div>
    </div>
  );
}
