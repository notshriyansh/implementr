interface Props {
  onPromptClick: (prompt: string) => void;
}

const prompts = [
  "Summarize this paper",
  "Explain the architecture",
  "What are the key innovations?",
  "How would I implement this in PyTorch?",
];

export function ChatEmptyState({ onPromptClick }: Props) {
  return (
    <div className="flex flex-col items-center justify-center h-full py-20">
      <h2 className="text-2xl font-semibold">
        Ask a question about this paper
      </h2>

      <p className="text-muted-foreground mt-2">
        Grounded answers using retrieved paper context.
      </p>

      <div className="grid grid-cols-2 gap-3 mt-8 w-full max-w-2xl">
        {prompts.map((prompt) => (
          <button
            key={prompt}
            onClick={() => onPromptClick(prompt)}
            className="text-left rounded-xl border p-4 hover:bg-muted/30 transition"
          >
            {prompt}
          </button>
        ))}
      </div>
    </div>
  );
}
