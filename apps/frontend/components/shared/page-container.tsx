"use client";

import { motion } from "framer-motion";

export function PageContainer({ children }: { children: React.ReactNode }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.35,
        ease: "easeOut",
      }}
      className="
        mx-auto
        w-full
        max-w-[1600px]
        px-8
        py-8
      "
    >
      {children}
    </motion.div>
  );
}
