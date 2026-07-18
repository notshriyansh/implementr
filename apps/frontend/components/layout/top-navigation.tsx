"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { navigationItems } from "@/lib/navigation";
import { cn } from "@/lib/utils";

export function TopNavigation() {
  const pathname = usePathname();

  return (
    <nav className="flex items-center gap-6 xl:gap-8">
      {navigationItems.map((item) => {
        const active = pathname.startsWith(item.href);

        return (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "group relative text-[11px] font-medium uppercase tracking-[0.08em] transition-colors duration-300",
              active
                ? "text-foreground"
                : "text-muted-foreground hover:text-foreground",
            )}
          >
            <span>{item.number}</span> <span>{item.label}</span>
            <span
              className={cn(
                "absolute -bottom-4.5 left-0 h-px bg-foreground transition-all duration-300",
                active ? "w-full" : "w-0 group-hover:w-full",
              )}
            />
          </Link>
        );
      })}
    </nav>
  );
}
