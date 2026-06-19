"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { cn } from "@/lib/utils";

const items = [
  {
    label: "Research",
    href: "/research",
    number: "01",
  },
  {
    label: "Repository",
    href: "/repository",
    number: "02",
  },
  {
    label: "Workspace",
    href: "/workspace",
    number: "03",
  },
  {
    label: "Evaluation",
    href: "/evaluation",
    number: "04",
  },
];

export function TopNavigation() {
  const pathname = usePathname();

  return (
    <nav className="flex items-center gap-8">
      {items.map((item) => {
        const active = pathname === item.href;

        return (
          <Link
            key={item.href}
            href={item.href}
            className={cn(
              "text-xs uppercase tracking-[0.18em] transition-colors",
              active
                ? "text-primary"
                : "text-muted-foreground hover:text-foreground",
            )}
          >
            {item.number} {item.label}
          </Link>
        );
      })}
    </nav>
  );
}
