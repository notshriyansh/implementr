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
        description="Select a file from the repository explorer."
      />
    );
  }

  return (
    <div
      className="
        rounded-3xl
        border
        border-border/50
        bg-card/40
        p-6
      "
    >
      <div className="border-b border-border/50 pb-5">
        <h2 className="break-all font-semibold">{file.path}</h2>

        <div className="mt-4 flex flex-wrap gap-2">
          <div className="rounded-full bg-muted px-3 py-1 text-xs">
            {file.imports.length} imports
          </div>

          <div className="rounded-full bg-muted px-3 py-1 text-xs">
            {file.functions.length} functions
          </div>

          <div className="rounded-full bg-muted px-3 py-1 text-xs">
            {file.classes.length} classes
          </div>
        </div>
      </div>

      <div className="mt-6 space-y-6">
        <Section
          title={`Imports (${file.imports.length})`}
          items={file.imports}
          emptyMessage="No imports detected"
        />

        <Section
          title={`Functions (${file.functions.length})`}
          items={file.functions}
          emptyMessage="No functions detected"
        />

        <Section
          title={`Classes (${file.classes.length})`}
          items={file.classes}
          emptyMessage="No classes detected"
        />
      </div>
    </div>
  );
}

function Section({
  title,
  items,
  emptyMessage,
}: {
  title: string;
  items: string[];
  emptyMessage: string;
}) {
  return (
    <div className="rounded-xl bg-muted/20 p-4">
      <h3 className="mb-3 font-medium">{title}</h3>

      {items.length === 0 ? (
        <p className="text-sm text-muted-foreground">{emptyMessage}</p>
      ) : (
        <ul className="space-y-2">
          {items.map((item) => (
            <li
              key={item}
              className="
                break-all
                rounded-lg
                bg-background/50
                px-3
                py-2
                font-mono
                text-sm
              "
            >
              {item}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
