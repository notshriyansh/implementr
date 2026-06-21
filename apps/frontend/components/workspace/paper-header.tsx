interface Props {
  paperId: string;
}

export function PaperHeader({ paperId }: Props) {
  return (
    <div className="mb-8">
      <div className="text-xs uppercase tracking-[0.2em] text-muted-foreground">
        Paper Workspace
      </div>

      <h1 className="text-3xl font-semibold mt-3">
        {decodeURIComponent(paperId)}
      </h1>

      <p className="text-muted-foreground mt-2">
        Explore research insights, ask grounded questions, and generate
        implementation guidance.
      </p>
    </div>
  );
}
