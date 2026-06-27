"use client";

import { useState } from "react";
import { ChevronRight, ChevronDown, Folder, FileCode } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

import { FileNode } from "@/types/repository";

import { TreeNode as TreeNodeType } from "@/lib/tree-builder";

interface Props {
  node: TreeNodeType;
  onSelect: (file: FileNode) => void;
}

export function TreeNode({ node, onSelect }: Props) {
  const [open, setOpen] = useState(true);

  if (node.type === "file") {
    return (
      <button
        onClick={() => node.file && onSelect(node.file as FileNode)}
        className="
          flex
          w-full
          items-center
          gap-2
          rounded-lg
          px-2
          py-1.5
          text-left
          text-sm
          hover:bg-muted/30
          transition-colors
        "
      >
        <FileCode className="h-4 w-4 text-muted-foreground" />

        <span className="truncate">{node.name}</span>
      </button>
    );
  }

  return (
    <div>
      <button
        onClick={() => setOpen(!open)}
        className="
          flex
          w-full
          items-center
          gap-2
          rounded-lg
          px-2
          py-1.5
          text-left
          hover:bg-muted/30
          transition-colors
        "
      >
        {open ? (
          <ChevronDown className="h-4 w-4" />
        ) : (
          <ChevronRight className="h-4 w-4" />
        )}

        <Folder className="h-4 w-4" />

        <span className="text-sm">{node.name}</span>
      </button>

      <AnimatePresence>
        {open && node.children && (
          <motion.div
            initial={{
              height: 0,
              opacity: 0,
            }}
            animate={{
              height: "auto",
              opacity: 1,
            }}
            exit={{
              height: 0,
              opacity: 0,
            }}
            className="ml-5 overflow-hidden"
          >
            {node.children.map((child) => (
              <TreeNode key={child.path} node={child} onSelect={onSelect} />
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
