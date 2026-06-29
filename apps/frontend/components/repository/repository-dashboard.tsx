import { FileNode } from "@/types/repository";

import { RepositoryStat } from "./repository-stat";

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
        <RepositoryStat
          label="Files"
          value={files.length}
          description="Indexed repository files"
        />

        <RepositoryStat
          label="Functions"
          value={totalFunctions}
          description="Detected functions"
        />

        <RepositoryStat
          label="Classes"
          value={totalClasses}
          description="Detected classes"
        />

        <RepositoryStat
          label="Imports"
          value={totalImports}
          description="Dependency references"
        />
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
                gap-4
                rounded-xl
                bg-muted/20
                px-4
                py-3
              "
            >
              <div className="min-w-0 flex-1">
                <div className="truncate font-medium">
                  {file.path.split(/[\\/]/).pop()}
                </div>

                <div className="truncate text-xs text-muted-foreground">
                  {file.path}
                </div>
              </div>

              <div
                className="
                  shrink-0
                  rounded-full
                  bg-background
                  px-3
                  py-1
                  text-xs
                  text-muted-foreground
                "
              >
                {file.functions.length + file.classes.length} symbols
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
