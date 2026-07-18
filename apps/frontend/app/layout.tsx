import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { ClerkProvider } from "@clerk/nextjs";

import "./globals.css";

import { QueryProvider } from "@/providers/query-provider";

import { Toaster } from "sonner";

import { CommandProvider } from "@/components/command/command-provider";
import { CommandPalette } from "@/components/command/command-palette";
import { AuthProvider } from "@/providers/auth-provider";

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
    <ClerkProvider>
      <html
        lang="en"
        className={`${geistSans.variable} ${geistMono.variable} h-full antialiased dark`}
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
