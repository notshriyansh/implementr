"use client";

import { useState } from "react";

import { Input } from "@/components/ui/input";

interface Props {
  onSearch: (query: string) => void;
}

export function RepositorySearch({ onSearch }: Props) {
  const [query, setQuery] = useState("");

  return (
    <Input
      value={query}
      onChange={(e) => {
        const value = e.target.value;

        setQuery(value);

        onSearch(value);
      }}
      placeholder="Search repository..."
      className="h-9 w-62.5 text-sm"
      aria-label="Search repository files"
    />
  );
}
