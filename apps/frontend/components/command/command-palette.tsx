"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import {
  CommandDialog,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
  CommandSeparator,
} from "@/components/ui/command";

import { useCommandPalette } from "./command-provider";

import { useAppStore } from "@/stores/app-store";

export function CommandPalette() {
  const router = useRouter();

  const { open, setOpen } = useCommandPalette();

  const recentQuestions = useAppStore((state) => state.recentQuestions);

  const recentRepositories = useAppStore((state) => state.recentRepositories);

  const recentPapers = useAppStore((state) => state.recentPapers);

  const selectedPaper = useAppStore((state) => state.selectedPaper);

  const selectedRepository = useAppStore((state) => state.selectedRepository);

  useEffect(() => {
    function handler(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key.toLowerCase() === "k") {
        e.preventDefault();

        setOpen((prev) => !prev);
      }
    }

    window.addEventListener("keydown", handler);

    return () => window.removeEventListener("keydown", handler);
  }, [setOpen]);

  function navigate(path: string) {
    router.push(path);

    setOpen(false);
  }

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="Search papers, repositories, commands..." />

      <CommandList>
        <CommandGroup heading="Navigation">
          <CommandItem onSelect={() => navigate("/research")}>
            Research
          </CommandItem>

          <CommandItem onSelect={() => navigate("/repository")}>
            Repository
          </CommandItem>

          <CommandItem onSelect={() => navigate("/architecture")}>
            Architecture
          </CommandItem>

          <CommandItem onSelect={() => navigate("/workspace")}>
            Workspace
          </CommandItem>
        </CommandGroup>

        <CommandSeparator />

        <CommandGroup heading="Actions">
          <CommandItem onSelect={() => navigate("/research")}>
            Search Papers
          </CommandItem>

          <CommandItem onSelect={() => navigate("/repository")}>
            Analyze Repository
          </CommandItem>

          <CommandItem onSelect={() => navigate("/architecture")}>
            Analyze Architecture
          </CommandItem>

          <CommandItem onSelect={() => navigate("/workspace")}>
            Hybrid Analysis
          </CommandItem>
        </CommandGroup>

        <CommandSeparator />

        <CommandGroup heading="Current Context">
          {selectedPaper && (
            <CommandItem>Paper: {selectedPaper.title}</CommandItem>
          )}

          {selectedRepository && (
            <CommandItem>Repository: {selectedRepository}</CommandItem>
          )}
        </CommandGroup>

        <CommandSeparator />

        <CommandGroup heading="Recent Papers">
          {recentPapers.length === 0 ? (
            <CommandItem disabled>No recent papers</CommandItem>
          ) : (
            recentPapers.map((paper) => (
              <CommandItem key={paper.pdf_url}>{paper.title}</CommandItem>
            ))
          )}
        </CommandGroup>

        <CommandSeparator />

        <CommandGroup heading="Recent Questions">
          {recentQuestions.length === 0 ? (
            <CommandItem disabled>No recent questions</CommandItem>
          ) : (
            recentQuestions.map((question) => (
              <CommandItem key={question}>{question}</CommandItem>
            ))
          )}
        </CommandGroup>

        <CommandSeparator />

        <CommandGroup heading="Recent Repositories">
          {recentRepositories.length === 0 ? (
            <CommandItem disabled>No recent repositories</CommandItem>
          ) : (
            recentRepositories.map((repo) => (
              <CommandItem key={repo}>{repo}</CommandItem>
            ))
          )}
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}
