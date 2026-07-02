"use client";

import { motion } from "framer-motion";

import { duration, ease } from "@/lib/motion";

export function PageContainer({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: duration.normal,
        ease: ease.enter,
      }}
      className="
        mx-auto
        w-full
        max-w-360
        px-4
        sm:px-6
        lg:px-8
        xl:px-10
        py-6
        lg:py-8
      "
    >
      {children}
    </motion.div>
  );
}
