import { FileNode } from "@/types/repository";

interface Props {
  file?: FileNode;
}

export function RepositoryCodeViewer({ file }: Props) {
  if (!file) {
    return (
      <div className="border rounded-xl h-full flex items-center justify-center text-muted-foreground">
        Select a file
      </div>
    );
  }

  return (
    <div className="border rounded-xl p-6">
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
