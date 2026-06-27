"use client";

import { FileNode } from "@/types/repository";

import { buildRepositoryTree } from "@/lib/tree-builder";

import { TreeNode } from "./tree-node";

interface Props {
  files: FileNode[];
  onSelect: (file: FileNode) => void;
}

export function RepositoryTree({ files, onSelect }: Props) {
  const tree = buildRepositoryTree(files);

  return (
    <div
      className="
        rounded-3xl
        border
        border-border/50
        bg-card/40
        backdrop-blur-sm
        overflow-hidden
      "
    >
      <div className="border-b px-4 py-3 font-medium">Repository Explorer</div>

      <div className="max-h-162.5 overflow-y-auto p-2">
        {tree.map((node) => (
          <TreeNode key={node.path} node={node} onSelect={onSelect} />
        ))}
      </div>
    </div>
  );
}
