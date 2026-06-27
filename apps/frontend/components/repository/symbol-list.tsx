interface Props {
  title: string;
  symbols: string[];
}

export function SymbolList({ title, symbols }: Props) {
  if (!symbols.length) return null;

  return (
    <div
      className="
        rounded-2xl
        border
        border-border/50
        bg-card/30
        p-5
      "
    >
      <h3 className="mb-4 font-medium">{title}</h3>

      <div className="space-y-2">
        {symbols.map((symbol) => (
          <div
            key={symbol}
            className="
              rounded-lg
              bg-muted/30
              px-3
              py-2
              font-mono
              text-sm
            "
          >
            {symbol}
          </div>
        ))}
      </div>
    </div>
  );
}
