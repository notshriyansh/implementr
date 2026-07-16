export function LandingFooter() {
  return (
    <footer className="border-t border-border">
      <div className="mx-auto flex max-w-7xl justify-between px-6 py-20">
        <div>
          <div className="text-2xl font-semibold">IMPLEMENTR</div>

          <p className="mt-6 max-w-sm text-muted-foreground">
            Architecture-aware implementation for modern ML systems.
          </p>
        </div>

        <div className="grid grid-cols-2 gap-16">
          <div>
            <div className="mb-4 text-xs uppercase tracking-widest text-muted-foreground">
              Product
            </div>

            <div className="space-y-2">
              <div>Research</div>
              <div>Repository</div>
              <div>Architecture</div>
              <div>Workspace</div>
            </div>
          </div>

          <div>
            <div className="mb-4 text-xs uppercase tracking-widest text-muted-foreground">
              Future
            </div>

            <div className="space-y-2">
              <div>Clerk Auth</div>
              <div>Projects</div>
              <div>Teams</div>
              <div>History</div>
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
}
