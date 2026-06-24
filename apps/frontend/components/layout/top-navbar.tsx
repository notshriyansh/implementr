"use client";

import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";
import { TopNavigation } from "./top-navigation";

export function TopNavbar() {
  return (
    <header className="sticky top-0 z-50 h-16 border-b border-border/50 bg-background/80 backdrop-blur-xl">
      <div className="max-w-[1600px] mx-auto px-8 h-full flex items-center justify-between">
        <div className="flex items-center gap-10">
          <div className="font-bold tracking-tight text-lg">IMPLEMENTR</div>

          <TopNavigation />
        </div>

        <div className="flex-1 flex justify-center px-10">
          <button className="w-full max-w-md flex items-center gap-3 rounded-xl border px-4 py-2 text-sm text-muted-foreground hover:bg-muted/30 transition-colors">
            <Search className="h-4 w-4" />

            <span>Search papers, repositories, symbols...</span>

            <span className="ml-auto text-xs border rounded px-1.5 py-0.5">
              ⌘K
            </span>
          </button>
        </div>

        <Button size="sm" className="rounded-full">
          Launch Workspace
        </Button>
      </div>
    </header>
  );
}
