"use client";

import { useEffect } from "react";
import { useAuth } from "@clerk/nextjs";

import { apiClient } from "@/services/api-client";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const { getToken } = useAuth();

  useEffect(() => {
    const interceptor = apiClient.interceptors.request.use(async (config) => {
      const token = await getToken();

      config.headers = config.headers ?? {};

      if (token) {
        config.headers.Authorization = `Bearer ${token}`;
      }

      return config;
    });

    return () => {
      apiClient.interceptors.request.eject(interceptor);
    };
  }, [getToken]);

  return <>{children}</>;
}
