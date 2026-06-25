"use client";

import {
  createContext,
  useContext,
  useState,
  Dispatch,
  SetStateAction,
} from "react";

interface CommandContextValue {
  open: boolean;
  setOpen: Dispatch<SetStateAction<boolean>>;
}

const CommandContext = createContext<CommandContextValue | null>(null);

export function CommandProvider({ children }: { children: React.ReactNode }) {
  const [open, setOpen] = useState(false);
  const value = {
    open,
    setOpen,
  };

  return (
    <CommandContext.Provider value={value}>{children}</CommandContext.Provider>
  );
}

export function useCommandPalette() {
  const context = useContext(CommandContext);

  if (!context) {
    throw new Error("useCommandPalette must be used inside CommandProvider");
  }

  return context;
}
