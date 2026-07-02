import { useState } from "react";
import { FileNode } from "@/types/repository";
import { EmptyState } from "../shared/empty-state";
import { useAppStore } from "@/stores/app-store";
import { useFileContent } from "@/hooks/use-file-content";
import { CodeViewer } from "../code/code-viewer";
import { Loader2 } from "lucide-react";

interface Props {
  file?: FileNode;
}

export function RepositoryCodeViewer({ file }: Props) {
  const [activeTab, setActiveTab] = useState<"code" | "overview">("code");
  const selectedRepository = useAppStore((state) => state.selectedRepository);

  const fileContentQuery = useFileContent(selectedRepository, file?.path);

  if (!file) {
    return (
      <EmptyState
        title="No file selected"
        description="Select a file from the repository explorer."
      />
    );
  }

  return (
    <div className="flex h-full w-full flex-col bg-background">
      <div className="flex items-center justify-between border-b border-border px-6 py-4">
        <div>
          <h2 className="break-all font-semibold">{file.path}</h2>
          {fileContentQuery.data && (
            <p className="mt-1 text-xs text-muted-foreground">
              {(fileContentQuery.data.size_bytes / 1024).toFixed(2)} KB •{" "}
              {fileContentQuery.data.line_count} lines
            </p>
          )}
        </div>

        <div className="flex rounded-lg bg-muted p-1">
          <button
            onClick={() => setActiveTab("code")}
            className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
              activeTab === "code"
                ? "bg-background text-foreground shadow-sm"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Code
          </button>
          <button
            onClick={() => setActiveTab("overview")}
            className={`rounded-md px-3 py-1.5 text-xs font-medium transition-colors ${
              activeTab === "overview"
                ? "bg-background text-foreground shadow-sm"
                : "text-muted-foreground hover:text-foreground"
            }`}
          >
            Overview
          </button>
        </div>
      </div>

      <div className="flex-1 overflow-hidden">
        {activeTab === "code" ? (
          fileContentQuery.isLoading ? (
            <div className="flex h-full items-center justify-center">
              <Loader2 className="h-6 w-6 animate-spin text-muted-foreground" />
            </div>
          ) : fileContentQuery.data ? (
            <CodeViewer
              code={fileContentQuery.data.content}
              language={fileContentQuery.data.language}
            />
          ) : (
            <div className="flex h-full items-center justify-center text-muted-foreground">
              Failed to load file content.
            </div>
          )
        ) : (
          <div className="h-full overflow-y-auto p-6 space-y-6">
            <div className="flex flex-wrap gap-2">
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
        )}
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
