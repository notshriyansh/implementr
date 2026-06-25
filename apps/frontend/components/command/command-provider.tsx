"use client";

import { createContext, useContext, useState } from "react";

interface CommandContextValue {
  open: boolean;
  setOpen: (open: boolean) => void;
}

const CommandContext = createContext<CommandContextValue | null>(null);

export function CommandProvider({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);

  return (
    <CommandContext.Provider
      value={{
        open,
        setOpen,
      }}
    >
      {children}
    </CommandContext.Provider>
  );
}

export function useCommandPalette() {
  const context = useContext(CommandContext);

  if (!context) {
    throw new Error("useCommandPalette must be used inside CommandProvider");
  }

  return context;
}
