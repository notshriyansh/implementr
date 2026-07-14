"use client";

import { useRouter } from "next/navigation";

import { Button } from "@/components/ui/button";

import { useAppStore } from "@/stores/app-store";

interface Props {
  filePath: string;
  symbolName: string;
}

export function OpenFileButton({ filePath, symbolName }: Props) {
  const router = useRouter();

  const setBlueprintTargetFile = useAppStore((s) => s.setBlueprintTargetFile);

  const setBlueprintTargetSymbol = useAppStore(
    (s) => s.setBlueprintTargetSymbol,
  );

  function handleOpen() {
    setBlueprintTargetFile(filePath);

    setBlueprintTargetSymbol(symbolName);

    router.push("/repository");
  }

  return (
    <Button size="sm" variant="outline" onClick={handleOpen}>
      Open File
    </Button>
  );
}
