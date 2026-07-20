import Link from "next/link";

const links = [
  {
    label: "Research",
    href: "/research",
  },
  {
    label: "Repository",
    href: "/repository",
  },
  {
    label: "Architecture",
    href: "/architecture",
  },
  {
    label: "Workspace",
    href: "/workspace",
  },
];

export function LandingFooter() {
  return (
    <footer className="border-t border-border">
      <div className="mx-auto flex max-w-7xl flex-col gap-12 px-6 py-16 md:flex-row md:justify-between">
        <div className="max-w-sm">
          <div className="text-lg font-medium tracking-tight">Implementr</div>

          <p className="mt-4 text-sm leading-7 text-muted-foreground">
            Repository-aware implementation assistant for turning research
            papers into production-ready engineering plans.
          </p>
        </div>

        <div className="flex flex-wrap gap-10">
          {links.map((link) => (
            <Link
              key={link.href}
              href={link.href}
              className="text-sm text-muted-foreground transition-colors hover:text-foreground"
            >
              {link.label}
            </Link>
          ))}
        </div>
      </div>

      <div className="border-t border-border">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <span className="font-mono text-xs text-muted-foreground">
            © {new Date().getFullYear()} Implementr
          </span>

          <span className="font-mono text-xs text-muted-foreground">
            Repository-aware implementation
          </span>
        </div>
      </div>
    </footer>
  );
}
