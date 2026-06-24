"use client";

import { Search } from "lucide-react";
import { Input } from "@/components/ui/input";

interface Props {
  value: string;
  onChange: (value: string) => void;
}

export function PaperSearchBar({ value, onChange }: Props) {
  return (
    <div className="relative">
      <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />

      <Input
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder="Search papers · arXiv ID · author · keyword"
        className="
          pl-10
          h-14
          rounded-2xl
          border-border/60
          bg-muted/20
          text-base
          transition-all
          focus-visible:ring-1
          "
      />
    </div>
  );
}
