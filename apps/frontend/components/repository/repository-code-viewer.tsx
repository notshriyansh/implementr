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
    <div className="rounded-3xl border border-border/50 bg-card/40 backdrop-blur-sm p-6">
      <h2 className="font-semibold text-lg">{file.path}</h2>

      <div className="mt-6 space-y-6">
        <section className="rounded-xl bg-muted/20 p-4">
          <h3 className="mb-3 font-medium">Imports</h3>

          <ul className="space-y-2">
            {file.imports.map((item) => (
              <li key={item} className="font-mono text-sm">
                {item}
              </li>
            ))}
          </ul>
        </section>

        <section className="rounded-xl bg-muted/20 p-4">
          <h3 className="mb-3 font-medium">Functions</h3>

          <ul className="space-y-2">
            {file.functions.map((item) => (
              <li key={item} className="font-mono text-sm">
                {item}
              </li>
            ))}
          </ul>
        </section>

        <section className="rounded-xl bg-muted/20 p-4">
          <h3 className="mb-3 font-medium">Classes</h3>

          <ul className="space-y-2">
            {file.classes.map((item) => (
              <li key={item} className="font-mono text-sm">
                {item}
              </li>
            ))}
          </ul>
        </section>
      </div>
    </div>
  );
}
