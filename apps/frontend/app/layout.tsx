import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";

import "./globals.css";

import { QueryProvider } from "@/providers/query-provider";

import { Toaster } from "sonner";

import { CommandProvider } from "@/components/command/command-provider";
import { CommandPalette } from "@/components/command/command-palette";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "Implementr",
  description: "AI-powered research to implementation platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
    >
      <body className="min-h-screen bg-background text-foreground">
        <QueryProvider>
          <CommandProvider>
            {children}

            <CommandPalette />

            <Toaster richColors position="top-right" />
          </CommandProvider>
        </QueryProvider>
      </body>
    </html>
  );
}
