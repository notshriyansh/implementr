import Link from "next/link";

const surfaces = [
  {
    number: "01",
    title: "Research",
    description:
      "Discover papers, ingest research and build implementation context.",
    href: "/research",
  },
  {
    number: "02",
    title: "Repository",
    description: "Search symbols, inspect files and understand code structure.",
    href: "/repository",
  },
  {
    number: "03",
    title: "Architecture",
    description: "Trace execution flows and identify modification points.",
    href: "/architecture",
  },
  {
    number: "04",
    title: "Workspace",
    description: "Generate implementation plans, blueprints and evaluations.",
    href: "/workspace",
  },
];

export function SurfaceGrid() {
  return (
    <section className="mx-auto max-w-7xl px-6 pb-32">
      <div className="mb-8 text-xs uppercase tracking-[0.25em] text-muted-foreground">
        Four Surfaces, One Workspace
      </div>

      <div className="grid overflow-hidden rounded-3xl border border-border md:grid-cols-2">
        {surfaces.map((surface) => (
          <Link
            key={surface.href}
            href={surface.href}
            className="border-border border-b md:border-r p-10 hover:bg-muted/10 transition-colors"
          >
            <div className="text-xs uppercase tracking-[0.25em] text-muted-foreground">
              {surface.number}
            </div>

            <h3 className="mt-8 text-4xl font-semibold">{surface.title}</h3>

            <p className="mt-4 max-w-md text-lg text-muted-foreground">
              {surface.description}
            </p>
          </Link>
        ))}
      </div>
    </section>
  );
}
