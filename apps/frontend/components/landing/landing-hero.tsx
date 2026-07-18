"use client";

import Link from "next/link";
import { motion } from "framer-motion";

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

export function LandingHero() {
  return (
    <section className="relative overflow-hidden">
      <div className="pointer-events-none absolute inset-0 hero-grid" />
      <div className="pointer-events-none absolute inset-0 hero-glow" />

      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="relative mx-auto max-w-7xl px-6 pt-28 pb-24 sm:pt-32 sm:pb-28 lg:pt-40 lg:pb-36"
      >
        <div className="max-w-4xl">
          <motion.div variants={item}>
            <div className="mb-8 inline-flex items-center rounded-full border border-border/60 px-4 py-1.5 text-[11px] uppercase tracking-[0.25em] text-muted-foreground">
              Research → Repository → Implementation
            </div>
          </motion.div>

          <motion.h1
            variants={item}
            className="max-w-5xl text-3xl font-semibold tracking-tighter sm:text-4xl md:text-5xl lg:text-6xl xl:text-[5.25rem] xl:leading-[1.05]"
          >
            Architecture-aware implementation for Engineers.
          </motion.h1>

          <motion.p
            variants={item}
            className="mt-6 text-base leading-7 text-muted-foreground sm:mt-8 sm:text-lg sm:leading-8 md:text-xl md:leading-9 max-w-2xl"
          >
            Move from research papers to production repositories with structured
            reasoning. Analyze symbols, trace execution flows, and generate
            implementation blueprints grounded in real codebases.
          </motion.p>

          <motion.div
            variants={item}
            className="mt-10 flex flex-col gap-3 sm:flex-row sm:gap-4 sm:mt-12"
          >
            <Button asChild size="lg" className="sm:px-8">
              <Link href="/research">Enter Workspace</Link>
            </Button>

            <Button asChild variant="outline" size="lg">
              <Link href="/workspace">See Workspace</Link>
            </Button>
          </motion.div>
        </div>
      </motion.div>
    </section>
  );
}
