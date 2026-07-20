"use client";

import Link from "next/link";
import { motion } from "framer-motion";
import { ArrowRight } from "lucide-react";

import { Button } from "@/components/ui/button";
import { duration, ease, stagger } from "@/lib/motion";

const container = {
  hidden: {},
  show: {
    transition: {
      staggerChildren: stagger.normal,
    },
  },
};

const item = {
  hidden: { opacity: 0, y: 14 },
  show: {
    opacity: 1,
    y: 0,
    transition: {
      duration: duration.slow,
      ease: ease.enter,
    },
  },
};

const pipeline = [
  "Research Paper",
  "Repository Analysis",
  "Implementation Blueprint",
];

export function LandingHero() {
  return (
    <section className="relative overflow-hidden border-b border-border/50">
      <div className="pointer-events-none absolute inset-0 hero-grid" />

      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="relative mx-auto max-w-7xl px-6 pt-28 pb-24 sm:pt-32 sm:pb-28 lg:pt-40 lg:pb-32"
      >
        <div className="max-w-5xl">
          <motion.div variants={item}>
            <span className="font-mono text-xs uppercase tracking-[0.28em] text-muted-foreground">
              Repository-aware implementation assistant
            </span>
          </motion.div>

          <motion.h1
            variants={item}
            className="mt-8 max-w-5xl text-4xl font-medium tracking-tighter sm:text-5xl lg:text-7xl lg:leading-[1.02]"
          >
            Bridge research papers
            <br />
            and production code.
          </motion.h1>

          <motion.p
            variants={item}
            className="mt-8 max-w-3xl text-lg leading-8 text-muted-foreground"
          >
            Implementr helps engineers understand research papers, navigate real
            repositories, and generate implementation plans grounded in existing
            codebases instead of generic LLM responses.
          </motion.p>

          <motion.div variants={item} className="mt-10 flex flex-wrap gap-4">
            <Button asChild size="lg">
              <Link href="/research">Enter Workspace</Link>
            </Button>

            <Button asChild variant="outline" size="lg">
              <Link href="/workspace">Explore Demo</Link>
            </Button>
          </motion.div>

          <motion.div
            variants={item}
            className="mt-20 flex flex-wrap items-center gap-4 text-sm"
          >
            {pipeline.map((step, index) => (
              <div key={step} className="flex items-center gap-4">
                <span className="font-mono text-muted-foreground">{step}</span>

                {index < pipeline.length - 1 && (
                  <ArrowRight className="h-4 w-4 text-muted-foreground/50" />
                )}
              </div>
            ))}
          </motion.div>
        </div>
      </motion.div>
    </section>
  );
}
