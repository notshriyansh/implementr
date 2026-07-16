"use client";

import { SearchX } from "lucide-react";
import { Button } from "@/components/ui/button";

interface EmptyStateProps {
  title: string;
  description: string;
  actionLabel?: string;
  onAction?: () => void;
  icon?: React.ReactNode;
}

export function EmptyState({
  title,
  description,
  actionLabel,
  onAction,
  icon = <SearchX className="h-7 w-7 text-muted-foreground" />,
}: EmptyStateProps) {
  return (
    <div className="rounded-lg border border-border bg-card py-16 px-6">
      <div className="mx-auto flex max-w-lg flex-col items-center text-center">
        <div className="mb-5 flex h-14 w-14 items-center justify-center rounded-xl bg-muted">
          {icon}
        </div>

        <h3 className="text-xl font-semibold tracking-tight">{title}</h3>

        <p className="mt-3 text-sm leading-7 text-muted-foreground">
          {description}
        </p>

        {actionLabel && onAction && (
          <Button className="mt-8 rounded-xl" onClick={onAction}>
            {actionLabel}
          </Button>
        )}
      </div>
    </div>
  );
}
