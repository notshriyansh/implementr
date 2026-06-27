export interface TreeNode {
  name: string;
  path: string;
  type: "file" | "folder";

  children?: TreeNode[];

  file?: {
    path: string;
    imports: string[];
    functions: string[];
    classes: string[];
  };
}

export function buildRepositoryTree(
  files: {
    path: string;
    imports: string[];
    functions: string[];
    classes: string[];
  }[],
): TreeNode[] {
  const root: TreeNode[] = [];

  for (const file of files) {
    const parts = file.path.split("/");

    let currentLevel = root;

    let currentPath = "";

    parts.forEach((part, index) => {
      currentPath += index === 0 ? part : `/${part}`;

      const isFile = index === parts.length - 1;

      let existing = currentLevel.find((node) => node.name === part);

      if (!existing) {
        existing = {
          name: part,
          path: currentPath,
          type: isFile ? "file" : "folder",
          children: isFile ? undefined : [],
          file: isFile ? file : undefined,
        };

        currentLevel.push(existing);
      }

      if (existing.children) {
        currentLevel = existing.children;
      }
    });
  }

  return root;
}
