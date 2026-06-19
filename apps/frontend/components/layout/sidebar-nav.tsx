"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { navigationItems } from "@/lib/navigation";
import { cn } from "@/lib/utils";

export function SidebarNav() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r bg-background">
      <div className="h-16 border-b flex items-center px-6">
        <span className="font-semibold tracking-tight text-lg">IMPLEMENTR</span>
      </div>

      <nav className="flex flex-col gap-1 p-4">
        {navigationItems.map((item) => {
          const active = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={cn(
                "group flex items-center gap-3 rounded-lg px-3 py-3 transition-colors",
                active
                  ? "bg-muted text-foreground"
                  : "text-muted-foreground hover:text-foreground hover:bg-muted/50",
              )}
            >
              <span className="text-xs font-mono">{item.number}</span>

              <span className="uppercase tracking-[0.15em] text-xs">
                {item.label}
              </span>
            </Link>
          );
        })}
      </nav>
    </aside>
  );
}
