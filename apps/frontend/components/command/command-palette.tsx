"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";

import {
  CommandDialog,
  CommandInput,
  CommandList,
  CommandGroup,
  CommandItem,
} from "@/components/ui/command";

import { useCommandPalette } from "./command-provider";

export function CommandPalette() {
  const router = useRouter();

  const { open, setOpen } = useCommandPalette();

  useEffect(() => {
    function down(e: KeyboardEvent) {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();

        setOpen(!open);
      }
    }

    document.addEventListener("keydown", down);

    return () => document.removeEventListener("keydown", down);
  }, [open, setOpen]);

  return (
    <CommandDialog open={open} onOpenChange={setOpen}>
      <CommandInput placeholder="Search everywhere..." />

      <CommandList>
        <CommandGroup heading="Navigation">
          <CommandItem onSelect={() => router.push("/research")}>
            Research
          </CommandItem>

          <CommandItem onSelect={() => router.push("/repository")}>
            Repository
          </CommandItem>

          <CommandItem onSelect={() => router.push("/workspace")}>
            Workspace
          </CommandItem>

          <CommandItem onSelect={() => router.push("/architecture")}>
            Architecture
          </CommandItem>
        </CommandGroup>
      </CommandList>
    </CommandDialog>
  );
}
