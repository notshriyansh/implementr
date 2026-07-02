import * as React from "react";
import { cn } from "@/lib/utils";

export interface PanelLayoutProps extends React.HTMLAttributes<HTMLDivElement> {
  left: React.ReactNode;
  center: React.ReactNode;
  right: React.ReactNode;
  header?: React.ReactNode;
  footer?: React.ReactNode;
}

export function PanelLayout({
  left,
  center,
  right,
  header,
  footer,
  className,
  ...props
}: PanelLayoutProps) {
  return (
    <div
      className={cn(
        "flex flex-col w-full h-[calc(100vh-52px)] overflow-hidden bg-background",
        className,
      )}
      {...props}
    >
      {header && (
        <div className="shrink-0 border-b border-border">{header}</div>
      )}

      <div className="flex-1 min-h-0 grid grid-cols-1 md:grid-cols-[minmax(240px,280px)_1fr] lg:grid-cols-[minmax(240px,280px)_1fr_minmax(260px,320px)] divide-y md:divide-y-0 md:divide-x divide-border">
        <div className="hidden md:flex flex-col min-h-0 h-full overflow-y-auto bg-card">
          {left}
        </div>

        <div className="flex flex-col min-h-0 h-full overflow-y-auto bg-background">
          {center}
        </div>

        <div className="hidden lg:flex flex-col min-h-0 h-full overflow-y-auto bg-card">
          {right}
        </div>
      </div>

      {footer && (
        <div className="shrink-0 border-t border-border">{footer}</div>
      )}
    </div>
  );
}
