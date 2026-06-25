import { FileNode } from "@/types/repository";
import { EmptyState } from "../shared/empty-state";

interface Props {
  file?: FileNode;
}

export function RepositoryCodeViewer({ file }: Props) {
  if (!file) {
    return (
      <EmptyState
        title="No file selected"
        description="Choose a repository file from the explorer to inspect imports, classes and functions."
      />
    );
  }

  return (
    <div className="rounded-3xl bg-card/40 backdrop-blur-sm border border-border/50 p-6">
      <h2 className="font-semibold">{file.path}</h2>

      <div className="mt-6 space-y-6">
        <div>
          <h3 className="font-medium mb-2">Imports</h3>

          <ul className="space-y-1">
            {file.imports.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="font-medium mb-2">Functions</h3>

          <ul className="space-y-1">
            {file.functions.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>

        <div>
          <h3 className="font-medium mb-2">Classes</h3>

          <ul className="space-y-1">
            {file.classes.map((item) => (
              <li key={item}>{item}</li>
            ))}
          </ul>
        </div>
      </div>
    </div>
  );
}
