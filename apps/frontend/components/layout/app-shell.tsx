import { TopNavbar } from "./top-navbar";

interface AppShellProps {
  children: React.ReactNode;
}

export function AppShell({ children }: AppShellProps) {
  return (
    <div className="flex flex-col min-h-screen bg-background">
      <TopNavbar />

      <main className="flex-1 overflow-y-auto">{children}</main>
    </div>
  );
}
