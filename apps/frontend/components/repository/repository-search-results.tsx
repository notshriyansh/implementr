import { CodeChunk } from "@/types/repository";

interface Props {
  results: CodeChunk[];
  onSelect: (chunk: CodeChunk) => void;
}

export function RepositorySearchResults({ results, onSelect }: Props) {
  return (
    <div className="border rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b font-medium">Search Results</div>

      {results.map((result) => (
        <button
          key={result.chunk_id}
          onClick={() => onSelect(result)}
          className="w-full text-left border-b px-4 py-4 hover:bg-muted/30"
        >
          <div className="font-medium text-sm">{result.file_path}</div>

          <div className="text-xs text-muted-foreground mt-2">
            Lines {result.start_line}-{result.end_line}
          </div>

          <pre className="text-xs mt-3 line-clamp-4 overflow-hidden">
            {result.content}
          </pre>
        </button>
      ))}
    </div>
  );
}
