"use client";

import * as React from "react";
import { FileCode2 } from "lucide-react";
import { cn } from "@/lib/utils";

export interface CodeViewerProps extends React.HTMLAttributes<HTMLDivElement> {
  code: string;
  language?: string;
  filename?: string;
  startLine?: number;
  highlightLines?: number[];
}

export function CodeViewer({
  code,
  language = "text",
  filename,
  startLine = 1,
  highlightLines = [],
  className,
  ...props
}: CodeViewerProps) {
  const lines = code.split("\n");

  return (
    <div
      className={cn(
        "flex flex-col overflow-hidden rounded-xl border border-border bg-(--code-surface)",
        className,
      )}
      {...props}
    >
      {filename && (
        <div className="flex items-center gap-2 border-b border-border/50 bg-black/20 px-4 py-2.5">
          <FileCode2 className="h-4 w-4 text-muted-foreground" />
          <span className="font-mono text-xs text-muted-foreground">
            {filename}
          </span>
          <div className="ml-auto flex items-center gap-2">
            <span className="rounded bg-black/20 px-2 py-0.5 font-mono text-[10px] uppercase text-muted-foreground">
              {language}
            </span>
          </div>
        </div>
      )}

      <div className="flex-1 overflow-auto bg-(--code-surface) py-4">
        {lines.length === 0 || (lines.length === 1 && lines[0] === "") ? (
          <div className="px-6 py-4 font-mono text-sm text-muted-foreground">
            No content available
          </div>
        ) : (
          <div className="min-w-max">
            {lines.map((line, index) => {
              const currentLineNumber = startLine + index;
              const isHighlighted = highlightLines.includes(currentLineNumber);

              return (
                <div
                  key={index}
                  className={cn(
                    "flex pr-4 hover:bg-white/2 transition-colors duration-75",
                    isHighlighted && "bg-amber-500/10 hover:bg-amber-500/15",
                  )}
                >
                  <div
                    className={cn(
                      "sticky left-0 min-w-14 shrink-0 select-none border-r border-border/30 bg-(--code-surface) px-4 text-right font-mono text-xs leading-6 text-muted-foreground/50",
                      isHighlighted &&
                        "text-amber-500/70 border-amber-500/30 bg-amber-500/5",
                    )}
                  >
                    {currentLineNumber}
                  </div>

                  <div className="pl-4 font-mono text-[13px] leading-6 text-foreground/90 whitespace-pre">
                    {line || " "}
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
