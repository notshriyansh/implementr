"use client";

import { useMemo, useState } from "react";

import { FileNode } from "@/types/repository";

import { buildRepositoryTree } from "@/lib/tree-builder";

import { TreeNode } from "./tree-node";
import { RepositoryTreeSearch } from "./repository-tree-search";

interface Props {
  files: FileNode[];
  onSelect: (file: FileNode) => void;
  selectedFile?: string;
}

export function RepositoryTree({ files, onSelect, selectedFile }: Props) {
  const [search, setSearch] = useState("");

  const filteredFiles = useMemo(() => {
    if (!search) return files;

    return files.filter((file) =>
      file.path.toLowerCase().includes(search.toLowerCase()),
    );
  }, [files, search]);

  const tree = buildRepositoryTree(filteredFiles);

  return (
    <div
      className="
        h-full
        w-full
        bg-card
      "
    >
      <div className="flex items-center justify-between border-b px-4 py-3">
        <span className="font-medium">Repository Explorer</span>

        <span className="text-xs text-muted-foreground">
          {files.length} files
        </span>
      </div>

      <RepositoryTreeSearch value={search} onChange={setSearch} />

      <div className="max-h-162.5 overflow-y-auto p-2">
        {tree.map((node) => (
          <TreeNode
            key={node.path}
            node={node}
            onSelect={onSelect}
            selectedFile={selectedFile}
          />
        ))}
      </div>
    </div>
  );
}
