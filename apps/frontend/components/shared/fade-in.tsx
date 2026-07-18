"use client";

import { motion, type HTMLMotionProps } from "framer-motion";

import { duration, ease } from "@/lib/motion";

interface FadeInProps extends HTMLMotionProps<"div"> {
  children: React.ReactNode;
  delay?: number;
  y?: number;
}

export function FadeIn({
  children,
  delay = 0,
  y = 16,
  ...props
}: FadeInProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y }}
      whileInView={{ opacity: 1, y: 0 }}
      viewport={{ once: true, margin: "-60px" }}
      transition={{
        duration: duration.normal,
        ease: ease.enter,
        delay,
      }}
      {...props}
    >
      {children}
    </motion.div>
  );
}
