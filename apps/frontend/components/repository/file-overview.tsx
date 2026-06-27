import { FileNode } from "@/types/repository";

import { FileMetrics } from "./file-metrics";
import { SymbolList } from "./symbol-list";

interface Props {
  file: FileNode;
}

export function FileOverview({ file }: Props) {
  return (
    <div className="space-y-6">
      <div>
        <h2 className="text-xl font-semibold break-all">{file.path}</h2>

        <p className="mt-2 text-sm text-muted-foreground">
          Repository file analysis and symbol overview.
        </p>
      </div>

      <FileMetrics
        imports={file.imports.length}
        functions={file.functions.length}
        classes={file.classes.length}
      />

      <SymbolList title="Imports" symbols={file.imports} />

      <SymbolList title="Functions" symbols={file.functions} />

      <SymbolList title="Classes" symbols={file.classes} />
    </div>
  );
}
