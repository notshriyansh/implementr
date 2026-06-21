import { CodeSymbol } from "@/types/repository";

interface Props {
  results: CodeSymbol[];
}

export function SymbolResults({ results }: Props) {
  return (
    <div className="border rounded-xl">
      {results.map((symbol) => (
        <div key={symbol.symbol_id} className="border-b p-4">
          <div className="font-medium">{symbol.symbol_name}</div>

          <div className="text-xs text-muted-foreground">
            {symbol.symbol_type}
          </div>

          <div className="text-xs mt-1">{symbol.file_path}</div>
        </div>
      ))}
    </div>
  );
}
