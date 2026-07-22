import { ChevronRight, FileCode2 } from "lucide-react";

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

  const implementationTargets = [...files]
    .sort(
      (a, b) =>
        b.functions.length +
        b.classes.length -
        (a.functions.length + a.classes.length),
    )
    .slice(0, 5);

  return (
    <aside className="space-y-12 p-6">
      <section>
        <div className="font-mono text-xs uppercase tracking-[0.28em] text-muted-foreground">
          Repository Overview
        </div>

        <div className="mt-8 space-y-6">
          <RepositoryStat
            label="Files"
            value={files.length}
            description="Indexed source files"
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
      </section>

      <section>
        <div className="flex items-center gap-2">
          <FileCode2 className="h-4 w-4 text-muted-foreground" />

          <div className="font-mono text-xs uppercase tracking-[0.28em] text-muted-foreground">
            Suggested Targets
          </div>
        </div>

        <div className="mt-6 space-y-2">
          {implementationTargets.map((file) => {
            const symbolCount = file.functions.length + file.classes.length;

            return (
              <div
                key={file.path}
                className="group rounded-xl border border-border bg-card p-4 transition-colors hover:bg-muted/20"
              >
                <div className="flex items-start justify-between gap-4">
                  <div className="min-w-0 flex-1">
                    <div className="truncate text-sm font-medium">
                      {file.path.split(/[\\/]/).pop()}
                    </div>

                    <div className="mt-1 truncate text-xs text-muted-foreground">
                      {file.path}
                    </div>
                  </div>

                  <ChevronRight className="mt-0.5 h-4 w-4 text-muted-foreground/40 transition-transform group-hover:translate-x-0.5" />
                </div>

                <div className="mt-4 flex items-center justify-between border-t border-border pt-3">
                  <span className="font-mono text-[11px] uppercase tracking-wider text-muted-foreground">
                    Symbols
                  </span>

                  <span className="text-sm font-medium">{symbolCount}</span>
                </div>
              </div>
            );
          })}
        </div>
      </section>
    </aside>
  );
}
