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
        h-full
        w-full
        bg-background
      "
    >
      <div
        className="
          border-b
          border-border
          px-5
          py-4
        "
      >
        <div className="break-all font-medium">{chunk.file_path}</div>

        <div className="mt-2 flex flex-wrap gap-2">
          <span className="rounded-full bg-muted px-3 py-1 text-xs">
            {chunk.language}
          </span>

          <span className="rounded-full bg-muted px-3 py-1 text-xs">
            Lines {chunk.start_line}-{chunk.end_line}
          </span>
        </div>
      </div>

      <div className="max-h-212.5 overflow-auto">
        <pre
          className="
            p-6
            font-mono
            text-sm
            leading-6
          "
        >
          <code>{chunk.content}</code>
        </pre>
      </div>
    </div>
  );
}
