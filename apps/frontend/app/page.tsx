import { LandingHero } from "@/components/landing/landing-hero";
import { WorkspacePreview } from "@/components/landing/workspace-preview";
import { SurfaceGrid } from "@/components/landing/surface-grid";
import { LandingFooter } from "@/components/landing/landing-footer";

export default function HomePage() {
  return (
    <main>
      <LandingHero />

      <WorkspacePreview />

      <SurfaceGrid />

      <LandingFooter />
    </main>
  );
}
