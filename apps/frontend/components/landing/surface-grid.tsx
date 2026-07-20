"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import {
  ArrowRight,
  FileSearch,
  FolderTree,
  Network,
  ClipboardList,
} from "lucide-react";

import { FadeIn } from "@/components/shared/fade-in";
import { duration, ease, stagger } from "@/lib/motion";

const steps = [
  {
    icon: FileSearch,
    title: "Research",
    description:
      "Search papers, ingest PDFs and extract implementation knowledge.",
    href: "/research",
  },
  {
    icon: FolderTree,
    title: "Repository",
    description:
      "Index repositories, inspect symbols and understand project structure.",
    href: "/repository",
  },
  {
    icon: Network,
    title: "Architecture",
    description:
      "Trace execution flows and identify where research fits into existing systems.",
    href: "/architecture",
  },
  {
    icon: ClipboardList,
    title: "Blueprint",
    description:
      "Generate implementation plans grounded in the repository instead of generic suggestions.",
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

const item = {
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
    <section className="mx-auto max-w-7xl px-6 pb-28">
      <FadeIn>
        <div className="max-w-3xl">
          <div className="font-mono text-xs uppercase tracking-[0.28em] text-muted-foreground">
            Workflow
          </div>

          <h2 className="mt-3 text-3xl font-medium tracking-tight">
            From paper to implementation,
            <br />
            one step at a time.
          </h2>

          <p className="mt-5 text-lg leading-8 text-muted-foreground">
            Each stage builds on the previous one, giving the model more context
            before generating implementation guidance.
          </p>
        </div>
      </FadeIn>

      <motion.div
        variants={container}
        initial="hidden"
        whileInView="show"
        viewport={{ once: true }}
        className="mt-14 grid gap-6 lg:grid-cols-4"
      >
        {steps.map((step, index) => {
          const Icon = step.icon;

          return (
            <motion.div variants={item} key={step.title}>
              <Link
                href={step.href}
                className="group flex h-full flex-col rounded-2xl border border-border bg-card p-7 transition-all duration-300 hover:border-foreground/15 hover:bg-muted/20"
              >
                <div className="flex items-center justify-between">
                  <Icon className="h-5 w-5 text-muted-foreground" />

                  <span className="font-mono text-xs text-muted-foreground">
                    0{index + 1}
                  </span>
                </div>

                <h3 className="mt-8 text-xl font-medium">{step.title}</h3>

                <p className="mt-3 flex-1 text-sm leading-7 text-muted-foreground">
                  {step.description}
                </p>

                <div className="mt-8 flex items-center text-sm text-muted-foreground transition-colors group-hover:text-foreground">
                  Explore
                  <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
                </div>
              </Link>
            </motion.div>
          );
        })}
      </motion.div>
    </section>
  );
}
