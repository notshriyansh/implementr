"use client";

import { motion } from "framer-motion";

interface Props {
  children: React.ReactNode;
}

export function PageContainer({ children }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{
        duration: 0.35,
        ease: "easeOut",
      }}
      className="p-8 max-w-[1600px] mx-auto w-full"
    >
      {children}
    </motion.div>
  );
}
