"use client";

import { useEffect, useState } from "react";
import type { Os } from "../lib/site";

// Detect the visitor's OS from the user agent. Returns null until mounted
// (so server and first client render agree), then a best-guess Os.
export function useOs(): Os | null {
  const [os, setOs] = useState<Os | null>(null);

  useEffect(() => {
    const ua = navigator.userAgent.toLowerCase();
    if (ua.includes("win")) setOs("windows");
    else if (ua.includes("mac")) setOs("macos");
    else setOs("linux");
  }, []);

  return os;
}
