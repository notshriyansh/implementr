export function RepositoryHeader() {
  return (
    <div className="flex items-center gap-4">
      <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-muted text-xs font-semibold">
        02
      </div>
      <div>
        <h1 className="text-sm font-medium leading-none">
          Repository Explorer
        </h1>
        <p className="text-xs text-muted-foreground mt-1">
          Analyze structure, search code, inspect symbols
        </p>
      </div>
    </div>
  );
}
