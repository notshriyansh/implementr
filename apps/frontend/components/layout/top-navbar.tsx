"use client";

import Link from "next/link";
import { useAppStore } from "@/stores/app-store";
import { useState, useEffect } from "react";

import { Search, Menu, X } from "lucide-react";

import { UserButton } from "@clerk/nextjs";

import { Button } from "@/components/ui/button";

import { TopNavigation } from "./top-navigation";
import { useCommandPalette } from "@/components/command/command-provider";
import { navigationItems } from "@/lib/navigation";
import { cn } from "@/lib/utils";

export function TopNavbar() {
  const { setOpen } = useCommandPalette();

  const startNewSession = useAppStore((state) => state.startNewSession);

  const selectedPaper = useAppStore((state) => state.selectedPaper);

  const selectedRepository = useAppStore((state) => state.selectedRepository);

  const sessionStartedAt = useAppStore((state) => state.sessionStartedAt);

  const [minutesRunning, setMinutesRunning] = useState(0);
  const [mobileOpen, setMobileOpen] = useState(false);

  useEffect(() => {
    if (!sessionStartedAt) return;

    const update = () => {
      setMinutesRunning(
        Math.max(
          1,
          Math.floor(
            (Date.now() - new Date(sessionStartedAt).getTime()) / 60000,
          ),
        ),
      );
    };

    update();

    const interval = setInterval(update, 60000);

    return () => clearInterval(interval);
  }, [sessionStartedAt]);

  return (
    <header className="sticky top-0 z-50 border-b border-border/50 bg-background/80 backdrop-blur-xl">
      <div className="mx-auto flex h-13 w-full max-w-[1800px] items-center gap-4 px-4 sm:px-6 lg:px-8">
        <div className="shrink-0 text-sm font-semibold tracking-tight">
          IMPLEMENTR
        </div>

        <div className="hidden lg:block shrink-0">
          <TopNavigation />
        </div>

        <div className="flex min-w-0 flex-1 justify-center">
          <button
            onClick={() => setOpen(true)}
            className="
              flex
              h-9
              w-full
              max-w-xl
              items-center
              gap-3
              rounded-xl
              border
              border-border
              bg-background
              px-4
              transition-colors
              hover:border-foreground/20
              focus-visible:outline-none
              focus-visible:ring-1
              focus-visible:ring-ring
              "
          >
            <Search className="h-4 w-4 shrink-0 text-muted-foreground" />

            <span className="hidden md:block truncate text-sm text-muted-foreground">
              Search papers, repositories, symbols...
            </span>

            <kbd className="ml-auto shrink-0 rounded-md border bg-muted px-2 py-1 text-xs hidden sm:inline-block">
              ⌘ K
            </kbd>
          </button>
        </div>

        <div className="hidden xl:flex items-center gap-4 text-xs text-muted-foreground">
          {selectedPaper && <span>Paper Loaded</span>}

          {selectedRepository && <span>Repository Loaded</span>}

          <span>{minutesRunning}m</span>
        </div>

        <div className="flex items-center gap-3 shrink-0">
          <Button
            className="hidden md:flex rounded-lg px-5"
            onClick={startNewSession}
          >
            New Workspace
          </Button>

          <UserButton
            appearance={{
              elements: {
                avatarBox: "h-9 w-9",
              },
            }}
          />

          <button
            onClick={() => setMobileOpen(!mobileOpen)}
            className="inline-flex lg:hidden h-9 w-9 items-center justify-center rounded-lg text-muted-foreground transition-colors hover:text-foreground focus-visible:outline-none focus-visible:ring-1 focus-visible:ring-ring"
            aria-label="Toggle navigation menu"
          >
            {mobileOpen ? (
              <X className="h-5 w-5" />
            ) : (
              <Menu className="h-5 w-5" />
            )}
          </button>
        </div>
      </div>

      {mobileOpen && (
        <nav className="border-t border-border/50 bg-background px-4 py-3 lg:hidden sm:px-6">
          <div className="flex flex-col gap-1">
            {navigationItems.map((item) => (
              <Link
                key={item.href}
                href={item.href}
                onClick={() => setMobileOpen(false)}
                className="flex items-center gap-3 rounded-lg px-3 py-3 text-sm text-muted-foreground transition-colors hover:text-foreground hover:bg-muted/50"
              >
                <span className="font-mono text-xs">{item.number}</span>
                <span className="uppercase tracking-widest text-xs">
                  {item.label}
                </span>
              </Link>
            ))}

            <div className="mt-2 flex gap-2 md:hidden">
              <Button
                className="flex-1 rounded-lg"
                onClick={() => {
                  startNewSession();
                  setMobileOpen(false);
                }}
              >
                New Workspace
              </Button>
            </div>
          </div>
        </nav>
      )}
    </header>
  );
}
