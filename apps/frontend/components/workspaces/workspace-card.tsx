import { motion } from "framer-motion";
import Link from "next/link";
import { Workspace } from "@/types/workspace";

interface Props {
  workspace: Workspace;
}

export function WorkspaceCard({ workspace }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.25,
      }}
    >
      <Link
        href={`/workspaces/${workspace.id}`}
        className="
        block
        rounded-lg
        border
        border-border
        bg-card
        p-5
        transition-all
        duration-200
        hover:bg-muted/30
        hover:border-foreground/15
      "
      >
        <h3 className="font-medium">{workspace.name}</h3>

        <p className="mt-2 text-sm text-muted-foreground">
          {workspace.selected_repository ?? "No repository selected"}
        </p>

        <p className="mt-2 text-xs text-muted-foreground">
          {workspace.workspace_question ?? "No question"}
        </p>

        {workspace.updated_at && (
          <p className="mt-3 text-xs text-muted-foreground">
            Last updated {new Date(workspace.updated_at).toLocaleDateString()}
          </p>
        )}
      </Link>
    </motion.div>
  );
}
