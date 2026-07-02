export const duration = {
  instant: 0.1,
  fast: 0.18,
  normal: 0.28,
  slow: 0.4,
} as const;

export const ease = {
  default: [0.25, 0.46, 0.45, 0.94] as const,
  enter: [0.0, 0.0, 0.2, 1.0] as const,
  exit: [0.4, 0.0, 1.0, 1.0] as const,
} as const;

export const stagger = {
  tight: 0.03,
  normal: 0.06,
  wide: 0.1,
} as const;
