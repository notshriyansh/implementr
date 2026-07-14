"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

import { cn } from "@/lib/utils";

const items = [
  { number: "01", label: "Research", href: "/research" },
  { number: "02", label: "Repository", href: "/repository" },
  { number: "03", label: "Architecture", href: "/architecture" },
  { number: "04", label: "Workspace", href: "/workspace" },
  { number: "05", label: "Reproduction", href: "/reproduction" },
  { number: "06", label: "Blueprints", href: "/blueprints" },
  { number: "07", label: "Evaluation", href: "/evaluation" },
];

export function TopNavigation() {
  const pathname = usePathname();

  return (
    <nav className="flex items-center gap-10">
      {items.map((item) => {
        const active = pathname.startsWith(item.href);

        return (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "group relative text-xs uppercase tracking-[0.12em] font-medium transition-colors duration-300",
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
