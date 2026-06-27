import { FileNode } from "@/types/repository";

import { RepositoryStat } from "./repository-stats";

interface Props {
  files: FileNode[];
}

export function RepositoryDashboard({ files }: Props) {
  const totalFunctions = files.reduce(
    (acc, file) => acc + file.functions.length,
    0,
  );

  const totalClasses = files.reduce(
    (acc, file) => acc + file.classes.length,
    0,
  );

  const totalImports = files.reduce(
    (acc, file) => acc + file.imports.length,
    0,
  );

  const complexFiles = [...files]
    .sort(
      (a, b) =>
        b.functions.length +
        b.classes.length -
        (a.functions.length + a.classes.length),
    )
    .slice(0, 5);

  return (
    <div className="space-y-6">
      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <RepositoryStat label="Files" value={files.length} />
        <RepositoryStat label="Functions" value={totalFunctions} />
        <RepositoryStat label="Classes" value={totalClasses} />
        <RepositoryStat label="Imports" value={totalImports} />
      </div>

      <div
        className="
          rounded-3xl
          border
          border-border/50
          bg-card/40
          p-6
        "
      >
        <h3 className="mb-4 font-medium">Most Complex Files</h3>

        <div className="space-y-3">
          {complexFiles.map((file) => (
            <div
              key={file.path}
              className="
                flex
                items-center
                justify-between
                rounded-xl
                bg-muted/20
                px-4
                py-3
              "
            >
              <span className="font-mono text-sm">{file.path}</span>

              <span className="text-sm text-muted-foreground">
                {file.functions.length + file.classes.length} symbols
              </span>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
