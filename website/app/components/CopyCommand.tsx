"use client";

import { useState } from "react";

export function CopyCommand({
  command,
  label,
}: {
  command: string;
  label?: string;
}) {
  const [copied, setCopied] = useState(false);

  async function copy() {
    try {
      await navigator.clipboard.writeText(command);
      setCopied(true);
      setTimeout(() => setCopied(false), 1600);
    } catch {
      // clipboard blocked (e.g. insecure context) — no-op
    }
  }

  return (
    <div className="group relative flex items-center gap-3 rounded-lg border border-border bg-black/40 px-4 py-3 font-mono text-sm">
      {label && (
        <span className="shrink-0 rounded bg-bg-elev px-1.5 py-0.5 text-[11px] uppercase tracking-wide text-fg-faint">
          {label}
        </span>
      )}
      <code className="min-w-0 flex-1 overflow-x-auto whitespace-nowrap text-fg-dim [scrollbar-width:none]">
        <span className="mr-2 select-none text-accent">$</span>
        {command}
      </code>
      <button
        onClick={copy}
        aria-label="Copy command"
        className="shrink-0 cursor-pointer rounded-md border border-border-bright bg-bg-elev px-2.5 py-1 text-xs text-fg-dim transition hover:border-accent hover:text-accent"
      >
        {copied ? "Copied" : "Copy"}
      </button>
    </div>
  );
}
