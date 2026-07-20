import type { Metadata } from "next";
import { Geist_Mono, Instrument_Sans } from "next/font/google";
import { ClerkProvider } from "@clerk/nextjs";

import "./globals.css";

import { QueryProvider } from "@/providers/query-provider";
import { Toaster } from "sonner";
import { CommandProvider } from "@/components/command/command-provider";
import { CommandPalette } from "@/components/command/command-palette";
import { AuthProvider } from "@/providers/auth-provider";

const instrumentSans = Instrument_Sans({
  subsets: ["latin"],
  variable: "--font-instrument",
});

const geistMono = Geist_Mono({
  subsets: ["latin"],
  variable: "--font-geist-mono",
});

export const metadata: Metadata = {
  title: "Implementr",
  description: "Repository-aware implementation platform",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <ClerkProvider>
      <html
        lang="en"
        className={`${instrumentSans.variable} ${geistMono.variable} h-full antialiased dark`}
      >
        <body className="min-h-screen bg-background text-foreground">
          <AuthProvider>
            <QueryProvider>
              <CommandProvider>
                {children}

                <CommandPalette />

                <Toaster richColors position="top-right" />
              </CommandProvider>
            </QueryProvider>
          </AuthProvider>
        </body>
      </html>
    </ClerkProvider>
  );
}
