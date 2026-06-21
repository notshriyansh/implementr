import { FileNode } from "@/types/repository";

interface Props {
  files: FileNode[];
  onSelect: (file: FileNode) => void;
}

export function RepositoryFileList({ files, onSelect }: Props) {
  return (
    <div className="border rounded-xl overflow-hidden">
      <div className="px-4 py-3 border-b font-medium">Files</div>

      <div className="max-h-150 overflow-y-auto">
        {files.map((file) => (
          <button
            key={file.path}
            onClick={() => onSelect(file)}
            className="w-full text-left px-4 py-3 border-b hover:bg-muted/30"
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
