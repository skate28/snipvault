"use client";

import { PLATFORMS } from "../lib/site";
import { useOs } from "./useOs";

export function OsDownload() {
  const os = useOs();
  const platform = os ? PLATFORMS[os] : null;

  return (
    <div className="flex flex-col items-center gap-3 sm:flex-row">
      <a
        href={platform ? platform.downloadUrl : "#install"}
        className="group inline-flex items-center gap-2.5 rounded-lg bg-accent-strong px-6 py-3.5 text-sm font-semibold text-[#04110e] shadow-lg shadow-accent-glow transition hover:bg-accent"
      >
        <DownloadIcon />
        {platform ? `Download for ${platform.label}` : "Download"}
      </a>
      <a
        href="#install"
        className="text-sm text-fg-dim underline-offset-4 transition hover:text-fg hover:underline"
      >
        {platform ? "Other platforms & install scripts" : "See all platforms"}
      </a>
    </div>
  );
}

function DownloadIcon() {
  return (
    <svg
      width="16"
      height="16"
      viewBox="0 0 16 16"
      fill="none"
      className="transition group-hover:translate-y-0.5"
      aria-hidden
    >
      <path
        d="M8 1v9m0 0L4.5 6.5M8 10l3.5-3.5M2 13.5h12"
        stroke="currentColor"
        strokeWidth="1.5"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  );
}
