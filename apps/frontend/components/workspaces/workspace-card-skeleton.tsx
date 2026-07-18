import { Skeleton } from "@/components/ui/skeleton";

export function WorkspaceCardSkeleton() {
  return (
    <div
      className="
        rounded-lg
        border
        border-border
        bg-card
        p-5
      "
    >
      <Skeleton className="h-5 w-64" />

      <Skeleton className="mt-4 h-4 w-96 max-w-full" />

      <Skeleton className="mt-3 h-3 w-80 max-w-full" />

      <Skeleton className="mt-5 h-3 w-28" />
    </div>
  );
}
