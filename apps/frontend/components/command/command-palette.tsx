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

export function CommandPalette() {
  const router = useRouter();

  const { open, setOpen } = useCommandPalette();

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

          <CommandItem onSelect={() => navigate("/evaluation")}>
            Evaluation
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

        <CommandGroup heading="Recent">
          <CommandItem>Attention Is All You Need</CommandItem>

          <CommandItem>FlashAttention</CommandItem>

          <CommandItem>Video Transformers</CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}
