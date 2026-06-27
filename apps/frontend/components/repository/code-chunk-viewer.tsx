import { CodeChunk } from "@/types/repository";

import { EmptyState } from "../shared/empty-state";

interface Props {
  chunk?: CodeChunk;
}

export function CodeChunkViewer({ chunk }: Props) {
  if (!chunk) {
    return (
      <EmptyState
        title="No code selected"
        description="Choose a search result to inspect the code chunk."
      />
    );
  }

  return (
    <div
      className="
        overflow-hidden
        rounded-3xl
        border
        border-border/50
        bg-card/40
        backdrop-blur-sm
      "
    >
      <div
        className="
          border-b
          border-border/50
          px-5
          py-4
        "
      >
        <div className="font-medium break-all">{chunk.file_path}</div>

        <div className="mt-1 flex gap-4 text-xs text-muted-foreground">
          <span>{chunk.language}</span>

          <span>
            Lines {chunk.start_line} - {chunk.end_line}
          </span>
        </div>
      </div>

      <pre
        className="
          overflow-x-auto
          p-6
          text-sm
        "
      >
        <code>{chunk.content}</code>
      </pre>
    </div>
  );
}
