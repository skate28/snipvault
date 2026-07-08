"use client";

import { useEffect, useState } from "react";
import { PIP_COMMAND, PLATFORMS, PLATFORM_ORDER, type Os } from "../lib/site";
import { CopyCommand } from "./CopyCommand";
import { useOs } from "./useOs";

export function InstallTabs() {
  const detected = useOs();
  const [active, setActive] = useState<Os>("windows");

  // Once we detect the visitor's OS, preselect that tab.
  useEffect(() => {
    if (detected) setActive(detected);
  }, [detected]);

  const platform = PLATFORMS[active];

  return (
    <div className="mx-auto w-full max-w-2xl overflow-hidden rounded-2xl border border-border bg-bg-card">
      <div className="flex border-b border-border">
        {PLATFORM_ORDER.map((id) => {
          const isActive = id === active;
          return (
            <button
              key={id}
              onClick={() => setActive(id)}
              className={`relative flex-1 cursor-pointer px-4 py-3.5 text-sm font-medium transition ${
                isActive
                  ? "text-fg"
                  : "text-fg-faint hover:text-fg-dim"
              }`}
            >
              {PLATFORMS[id].label}
              {id === detected && (
                <span className="ml-1.5 align-middle text-[10px] text-accent">●</span>
              )}
              {isActive && (
                <span className="absolute inset-x-4 -bottom-px h-0.5 rounded-full bg-accent" />
              )}
            </button>
          );
        })}
      </div>

      <div className="space-y-6 p-6">
        <div>
          <p className="mb-2 text-xs font-medium uppercase tracking-wide text-fg-faint">
            One-line install
          </p>
          <CopyCommand
            command={platform.installCommand}
            label={platform.installLabel}
          />
        </div>

        <div className="flex items-center gap-4">
          <span className="h-px flex-1 bg-border" />
          <span className="text-xs text-fg-faint">or</span>
          <span className="h-px flex-1 bg-border" />
        </div>

        <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <p className="text-sm font-medium text-fg">Direct download</p>
            <p className="font-mono text-xs text-fg-faint">{platform.binaryName}</p>
          </div>
          <a
            href={platform.downloadUrl}
            className="inline-flex shrink-0 items-center justify-center gap-2 rounded-lg border border-border-bright bg-bg-elev px-4 py-2.5 text-sm font-medium text-fg transition hover:border-accent hover:text-accent"
          >
            Download binary
          </a>
        </div>

        <div className="rounded-lg border border-border/60 bg-black/20 p-4">
          <p className="mb-2 text-xs text-fg-faint">
            Already have Python? Install from source with pip:
          </p>
          <CopyCommand command={PIP_COMMAND} label="pip" />
        </div>
      </div>
    </div>
  );
}
