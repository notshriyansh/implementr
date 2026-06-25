import { FileNode } from "@/types/repository";

interface Props {
  files: FileNode[];
  onSelect: (file: FileNode) => void;
}

export function RepositoryFileList({ files, onSelect }: Props) {
  return (
    <div className="rounded-3xl overflow-hidden bg-card/40 backdrop-blur-sm border border-border/50">
      <div className="px-4 py-3 border-b font-medium">Files</div>

      <div className="max-h-162.5 overflow-y-auto">
        {files.map((file) => (
          <button
            key={file.path}
            onClick={() => onSelect(file)}
            className="w-full text-left px-4 py-3 border-b hover:bg-muted/20 transition-all duration-200"
          >
            <div className="text-sm">{file.path}</div>

            <div className="text-xs text-muted-foreground mt-1">
              {file.functions.length} functions · {file.classes.length} classes
            </div>
          </button>
        ))}
      </div>
    </div>
  );
}
