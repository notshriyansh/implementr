import { Search } from "lucide-react";
import { Button } from "@/components/ui/button";

export function TopNavbar() {
  return (
    <header className="h-16 border-b flex items-center justify-between px-6">
      <div className="w-full max-w-md">
        <button className="w-full flex items-center gap-3 rounded-lg border bg-background px-4 py-2 text-sm text-muted-foreground hover:bg-muted/40 transition-colors">
          <Search className="h-4 w-4" />
          <span>Search papers, repositories, symbols...</span>

          <span className="ml-auto text-xs border rounded px-1.5 py-0.5">
            ⌘K
          </span>
        </button>
      </div>

      <Button size="sm" className="rounded-full">
        Launch Workspace
      </Button>
    </header>
  );
}
