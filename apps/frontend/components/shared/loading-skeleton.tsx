import { Skeleton } from "@/components/ui/skeleton";

export function LoadingSkeleton() {
  return (
    <div className="rounded-xl border overflow-hidden">
      {Array.from({ length: 6 }).map((_, index) => (
        <div key={index} className="grid grid-cols-12 gap-4 px-6 py-6 border-b">
          <div className="col-span-7 space-y-3">
            <Skeleton className="h-4 w-24" />

            <Skeleton className="h-5 w-4/5" />

            <Skeleton className="h-4 w-2/5" />
          </div>

          <div className="col-span-2 flex gap-2">
            <Skeleton className="h-6 w-16 rounded-full" />

            <Skeleton className="h-6 w-16 rounded-full" />
          </div>

          <div className="col-span-2">
            <Skeleton className="h-6 w-24 rounded-full" />
          </div>

          <div className="col-span-1 flex justify-end">
            <Skeleton className="h-9 w-20 rounded-xl" />
          </div>
        </div>
      ))}
    </div>
  );
}
