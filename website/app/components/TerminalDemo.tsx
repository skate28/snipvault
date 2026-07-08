"use client";

import { useEffect, useRef, useState } from "react";

type Line = { text: string; kind: "cmd" | "out" | "ok" };

const SCRIPT: Line[] = [
  { text: `snipvault add "jwt decode" "jwt.decode(t, key)" --lang python --tags auth`, kind: "cmd" },
  { text: "added snippet 7: jwt decode", kind: "ok" },
  { text: "snipvault search auth", kind: "cmd" },
  { text: "   7  jwt decode            python      auth", kind: "out" },
  { text: "snipvault show 7", kind: "cmd" },
  { text: "jwt.decode(t, key)", kind: "out" },
];

// Typing animation that cycles through the script and loops.
export function TerminalDemo() {
  const [lines, setLines] = useState<{ text: string; kind: Line["kind"] }[]>([]);
  const [typing, setTyping] = useState("");
  const idx = useRef(0);
  const timers = useRef<ReturnType<typeof setTimeout>[]>([]);

  useEffect(() => {
    let cancelled = false;
    const wait = (ms: number) =>
      new Promise<void>((res) => {
        const t = setTimeout(res, ms);
        timers.current.push(t);
      });

    async function run() {
      while (!cancelled) {
        const line = SCRIPT[idx.current];
        if (line.kind === "cmd") {
          setTyping("");
          for (let i = 0; i < line.text.length && !cancelled; i++) {
            setTyping(line.text.slice(0, i + 1));
            await wait(28);
          }
          await wait(360);
          if (cancelled) return;
          setLines((prev) => [...prev, line]);
          setTyping("");
        } else {
          setLines((prev) => [...prev, line]);
          await wait(520);
        }
        idx.current = (idx.current + 1) % SCRIPT.length;
        if (idx.current === 0) {
          await wait(1600);
          if (cancelled) return;
          setLines([]);
        }
      }
    }

    run();
    return () => {
      cancelled = true;
      timers.current.forEach(clearTimeout);
    };
  }, []);

  return (
    <div className="overflow-hidden rounded-xl border border-border-bright bg-[#0b0d13] shadow-2xl shadow-black/60">
      <div className="flex items-center gap-2 border-b border-border bg-bg-elev px-4 py-2.5">
        <span className="h-3 w-3 rounded-full bg-[#ff5f57]" />
        <span className="h-3 w-3 rounded-full bg-[#febc2e]" />
        <span className="h-3 w-3 rounded-full bg-[#28c840]" />
        <span className="ml-2 font-mono text-xs text-fg-faint">snipvault — zsh</span>
      </div>
      <div className="h-64 space-y-1.5 overflow-hidden p-5 font-mono text-[13px] leading-relaxed sm:text-sm">
        {lines.map((l, i) => (
          <Row key={i} line={l} />
        ))}
        {typing !== "" && (
          <div>
            <span className="mr-2 select-none text-accent">$</span>
            <span className="text-fg">{typing}</span>
            <span className="cursor-blink text-accent">▋</span>
          </div>
        )}
      </div>
    </div>
  );
}

function Row({ line }: { line: { text: string; kind: Line["kind"] } }) {
  if (line.kind === "cmd") {
    return (
      <div>
        <span className="mr-2 select-none text-accent">$</span>
        <span className="text-fg">{line.text}</span>
      </div>
    );
  }
  return (
    <div className={line.kind === "ok" ? "text-term-green" : "text-fg-dim"}>
      {line.text}
    </div>
  );
}
