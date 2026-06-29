"use client";

import { useState } from "react";
import {
  ChevronRight,
  ChevronDown,
  Folder,
  FileCode,
  FileJson,
  FileType,
  FileText,
} from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

import { FileNode } from "@/types/repository";
import { TreeNode as TreeNodeType } from "@/lib/tree-builder";

interface Props {
  node: TreeNodeType;
  onSelect: (file: FileNode) => void;
  selectedFile?: string;
}

export function TreeNode({ node, onSelect, selectedFile }: Props) {
  const [open, setOpen] = useState(false);

  function getFileIcon(filename: string) {
    if (filename.endsWith(".ts") || filename.endsWith(".tsx")) {
      return <FileType className="h-4 w-4" />;
    }

    if (filename.endsWith(".py")) {
      return <FileCode className="h-4 w-4" />;
    }

    if (filename.endsWith(".json")) {
      return <FileJson className="h-4 w-4" />;
    }

    return <FileText className="h-4 w-4" />;
  }

  if (node.type === "file") {
    const active = node.file?.path === selectedFile;

    return (
      <button
        onClick={() => node.file && onSelect(node.file as FileNode)}
        className={`
          flex
          w-full
          items-center
          gap-2
          rounded-lg
          px-2
          py-1.5
          text-left
          text-sm
          transition-colors
          ${
            active
              ? "border-l-2 border-primary bg-muted font-medium"
              : "hover:bg-muted/30"
          }
        `}
      >
        <div className="text-muted-foreground">{getFileIcon(node.name)}</div>

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

        <Folder className="h-4 w-4 text-muted-foreground" />

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
            transition={{
              duration: 0.2,
            }}
            className="ml-5 overflow-hidden"
          >
            {node.children.map((child) => (
              <TreeNode
                key={child.path}
                node={child}
                onSelect={onSelect}
                selectedFile={selectedFile}
              />
            ))}
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
