import Link from "next/link";

const productLinks = [
  { label: "Research", href: "/research" },
  { label: "Repository", href: "/repository" },
  { label: "Architecture", href: "/architecture" },
  { label: "Workspace", href: "/workspace" },
];

const resourceLinks = [
  { label: "Documentation", href: "#" },
  { label: "GitHub", href: "#" },
  { label: "Changelog", href: "#" },
  { label: "Status", href: "#" },
];

export function LandingFooter() {
  return (
    <footer className="border-t border-border">
      <div className="mx-auto max-w-7xl px-6 py-14 sm:py-20">
        <div className="flex flex-col gap-12 md:flex-row md:justify-between">
          <div className="max-w-xs">
            <div className="text-sm font-semibold tracking-tight">
              IMPLEMENTR
            </div>

            <p className="mt-4 text-sm leading-relaxed text-muted-foreground">
              Architecture-aware implementation for modern ML systems.
            </p>
          </div>

          <div className="grid grid-cols-2 gap-12 sm:gap-16">
            <div>
              <div className="mb-4 text-[11px] uppercase tracking-widest text-muted-foreground">
                Product
              </div>

              <div className="space-y-2.5">
                {productLinks.map((link) => (
                  <div key={link.href}>
                    <Link
                      href={link.href}
                      className="text-sm text-muted-foreground transition-colors duration-200 hover:text-foreground"
                    >
                      {link.label}
                    </Link>
                  </div>
                ))}
              </div>
            </div>

            <div>
              <div className="mb-4 text-[11px] uppercase tracking-widest text-muted-foreground">
                Resources
              </div>

              <div className="space-y-2.5">
                {resourceLinks.map((link) => (
                  <div key={link.label}>
                    <a
                      href={link.href}
                      className="text-sm text-muted-foreground transition-colors duration-200 hover:text-foreground"
                    >
                      {link.label}
                    </a>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="border-t border-border">
        <div className="mx-auto flex max-w-7xl items-center justify-between px-6 py-5">
          <span className="text-xs text-muted-foreground">
            © {new Date().getFullYear()} Implementr
          </span>
        </div>
      </div>
    </footer>
  );
}
