"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowUpRight } from "lucide-react";

import { FadeIn } from "@/components/shared/fade-in";
import { duration, ease, stagger } from "@/lib/motion";

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

const container = {
  hidden: {},
  show: {
    transition: {
      staggerChildren: stagger.normal,
    },
  },
};

const cardVariant = {
  hidden: { opacity: 0, y: 16 },
  show: {
    opacity: 1,
    y: 0,
    transition: {
      duration: duration.normal,
      ease: ease.enter,
    },
  },
};

export function SurfaceGrid() {
  return (
    <section className="mx-auto max-w-7xl px-6 pb-24 sm:pb-32">
      <FadeIn>
        <div className="mb-8 text-xs uppercase tracking-[0.25em] text-muted-foreground">
          Four Surfaces, One Workspace
        </div>
      </FadeIn>

      <motion.div
        variants={container}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true, margin: "-80px" }}
        className="grid gap-px overflow-hidden rounded-2xl border border-border bg-border sm:rounded-3xl md:grid-cols-2"
      >
        {surfaces.map((surface) => (
          <motion.div key={surface.href} variants={cardVariant}>
            <Link
              href={surface.href}
              className="group relative flex flex-col bg-background p-8 transition-all duration-300 hover:bg-muted/10 lg:p-10"
            >
              <div className="flex items-center justify-between">
                <div className="font-mono text-xs text-muted-foreground">
                  {surface.number}
                </div>

                <ArrowUpRight className="h-4 w-4 text-muted-foreground/0 transition-all duration-300 group-hover:text-muted-foreground group-hover:translate-x-0.5 group-hover:-translate-y-0.5" />
              </div>

              <h3 className="mt-6 text-2xl font-semibold sm:mt-8 sm:text-3xl lg:text-4xl">
                {surface.title}
              </h3>

              <p className="mt-3 max-w-md text-base text-muted-foreground sm:mt-4 sm:text-lg">
                {surface.description}
              </p>
            </Link>
          </motion.div>
        ))}
      </motion.div>
    </section>
  );
}
