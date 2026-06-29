import { CodeChunk } from "@/types/repository";

interface Props {
  results: CodeChunk[];
  onSelect: (chunk: CodeChunk) => void;
}

export function RepositorySearchResults({ results, onSelect }: Props) {
  return (
    <div
      className="
        overflow-hidden
        rounded-3xl
        border
        border-border/50
        bg-card/40
      "
    >
      <div
        className="
          flex
          items-center
          justify-between
          border-b
          border-border/50
          px-5
          py-4
        "
      >
        <h2 className="font-medium">Search Results</h2>

        <span className="text-xs text-muted-foreground">
          {results.length} matches
        </span>
      </div>

      <div className="max-h-200 overflow-y-auto">
        {results.map((result) => (
          <button
            key={result.chunk_id}
            onClick={() => onSelect(result)}
            className="
              w-full
              border-b
              border-border/30
              px-5
              py-4
              text-left
              transition-colors
              hover:bg-muted/20
            "
          >
            <div className="min-w-0">
              <div className="truncate font-medium">
                {result.file_path.split(/[\\/]/).pop()}
              </div>

              <div className="truncate text-xs text-muted-foreground">
                {result.file_path}
              </div>
            </div>

            <div className="mt-3 flex gap-4 text-xs text-muted-foreground">
              <span>{result.language}</span>

              <span>
                Lines {result.start_line}-{result.end_line}
              </span>
            </div>

            <pre
              className="
                mt-3
                overflow-hidden
                rounded-lg
                bg-muted/20
                p-3
                text-xs
                line-clamp-4
              "
            >
              {result.content}
            </pre>
          </button>
        ))}
      </div>
    </div>
  );
}
