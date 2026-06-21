import { CodeChunk } from "@/types/repository";

interface Props {
  chunk?: CodeChunk;
}

export function CodeChunkViewer({ chunk }: Props) {
  if (!chunk) {
    return (
      <div className="border rounded-xl h-full flex items-center justify-center text-muted-foreground">
        Select a search result
      </div>
    );
  }

  return (
    <div className="border rounded-xl overflow-hidden">
      <div className="border-b px-4 py-3">{chunk.file_path}</div>

      <pre className="p-6 overflow-auto text-sm">
        <code>{chunk.content}</code>
      </pre>
    </div>
  );
}
