"use client";

import { Search } from "lucide-react";

import { Button } from "@/components/ui/button";

import { TopNavigation } from "./top-navigation";
import { useCommandPalette } from "@/components/command/command-provider";

export function TopNavbar() {
  const { setOpen } = useCommandPalette();

  return (
    <header className="sticky top-0 z-50 border-b border-border/50 bg-background/80 backdrop-blur-xl">
      <div className="mx-auto flex h-16 max-w-[1600px] items-center gap-8 px-8">
        <div className="shrink-0 text-lg font-bold tracking-tight">
          IMPLEMENTR
        </div>

        <div className="shrink-0">
          <TopNavigation />
        </div>

        <div className="min-w-0 flex flex-1 justify-center">
          <button
            onClick={() => setOpen(true)}
            className="
              flex
              h-11
              w-full
              max-w-xl
              items-center
              gap-3
              rounded-2xl
              border
              border-border/60
              bg-background
              px-4
              transition-all
              duration-300
              hover:border-foreground/20
              hover:shadow-md
            "
          >
            <Search className="h-4 w-4 shrink-0 text-muted-foreground" />

            <span className="truncate text-sm text-muted-foreground">
              Search papers, repositories, symbols...
            </span>

            <kbd className="ml-auto shrink-0 rounded-md border bg-muted px-2 py-1 text-xs">
              ⌘K
            </kbd>
          </button>
        </div>

        <Button size="sm" className="shrink-0 rounded-full px-5">
          Launch Workspace
        </Button>
      </div>
    </header>
  );
}
