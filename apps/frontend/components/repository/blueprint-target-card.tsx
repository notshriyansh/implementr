"use client";

import { useAppStore } from "@/stores/app-store";

export function BlueprintTargetCard() {
  const file = useAppStore((s) => s.blueprintTargetFile);

  const symbol = useAppStore((s) => s.blueprintTargetSymbol);

  const reason = useAppStore((s) => s.blueprintTargetReason);

  if (!file) {
    return null;
  }

  return (
    <div className="rounded-xl border border-border bg-card p-4">
      <div className="mb-3 text-xs uppercase tracking-wider text-muted-foreground">
        Blueprint Target
      </div>

      <div className="space-y-3">
        <div>
          <div className="text-xs text-muted-foreground">Symbol</div>

          <div className="font-mono text-sm">{symbol}</div>
        </div>

        <div>
          <div className="text-xs text-muted-foreground">File</div>

          <div className="break-all font-mono text-sm">{file}</div>
        </div>

        <div>
          <div className="text-xs text-muted-foreground">Why Modify</div>

          <div className="text-sm">{reason}</div>
        </div>
      </div>
    </div>
  );
}
