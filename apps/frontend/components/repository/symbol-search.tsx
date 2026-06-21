"use client";

import { useState } from "react";

import { Input } from "@/components/ui/input";

interface Props {
  onSearch: (query: string) => void;
}

export function SymbolSearch({ onSearch }: Props) {
  const [value, setValue] = useState("");

  return (
    <Input
      value={value}
      onChange={(e) => {
        const q = e.target.value;

        setValue(q);

        onSearch(q);
      }}
      placeholder="Search symbols..."
    />
  );
}
