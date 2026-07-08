import { VERSION } from "../lib/site";
import { OsDownload } from "./OsDownload";
import { TerminalDemo } from "./TerminalDemo";

export function Hero() {
  return (
    <section id="top" className="relative overflow-hidden">
      <div className="pointer-events-none absolute inset-0 backdrop-grid" />
      <div className="pointer-events-none absolute inset-x-0 top-0 h-[500px] glow" />

      <div className="relative mx-auto grid max-w-6xl items-center gap-12 px-5 pb-20 pt-16 lg:grid-cols-2 lg:pt-24">
        <div className="fade-up">
          <a
            href="#install"
            className="mb-6 inline-flex items-center gap-2 rounded-full border border-border bg-bg-elev px-3 py-1 text-xs text-fg-dim transition hover:border-accent"
          >
            <span className="h-1.5 w-1.5 rounded-full bg-accent" />
            {VERSION} — now with one-line installers
          </a>

          <h1 className="text-balance text-4xl font-bold leading-[1.1] tracking-tight sm:text-5xl lg:text-6xl">
            Your code snippets,
            <br />
            <span className="bg-gradient-to-r from-accent to-accent-strong bg-clip-text text-transparent">
              one command away.
            </span>
          </h1>

          <p className="mt-6 max-w-md text-lg leading-relaxed text-fg-dim">
            A tiny, dependency-free command-line vault for the code you keep
            re-Googling. Save it once, search it forever — all offline, all local.
          </p>

          <div className="mt-8">
            <OsDownload />
          </div>

          <p className="mt-4 font-mono text-xs text-fg-faint">
            Windows · macOS · Linux · no runtime required
          </p>
        </div>

        <div className="fade-up [animation-delay:120ms]">
          <TerminalDemo />
        </div>
      </div>
    </section>
  );
}
