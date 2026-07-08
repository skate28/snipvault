import { GITHUB_URL, VERSION } from "../lib/site";
import { Logo } from "./Logo";

export function Nav() {
  return (
    <header className="sticky top-0 z-50 border-b border-border/60 bg-bg/80 backdrop-blur-md">
      <nav className="mx-auto flex h-16 max-w-6xl items-center justify-between px-5">
        <div className="flex items-center gap-2.5">
          <a href="/" className="flex items-center gap-2.5">
            <Logo className="h-7 w-7" />
            <span className="font-semibold tracking-tight">Snippet Vault</span>
          </a>
          <a
            href="/versions"
            className="hidden rounded-full border border-border bg-bg-elev px-2 py-0.5 font-mono text-[11px] text-fg-faint transition hover:border-accent hover:text-accent sm:inline"
          >
            {VERSION}
          </a>
        </div>
        <div className="flex items-center gap-6 text-sm text-fg-dim">
          <a href="/#install" className="hidden transition hover:text-fg sm:inline">
            Install
          </a>
          <a href="/#features" className="hidden transition hover:text-fg sm:inline">
            Features
          </a>
          <a href="/#usage" className="hidden transition hover:text-fg sm:inline">
            Usage
          </a>
          <a href="/versions" className="hidden transition hover:text-fg sm:inline">
            Versions
          </a>
          <a
            href={GITHUB_URL}
            target="_blank"
            rel="noreferrer"
            className="inline-flex items-center gap-1.5 rounded-lg border border-border-bright bg-bg-elev px-3 py-1.5 font-medium text-fg transition hover:border-accent hover:text-accent"
          >
            <GithubMark />
            GitHub
          </a>
        </div>
      </nav>
    </header>
  );
}

function GithubMark() {
  return (
    <svg width="15" height="15" viewBox="0 0 16 16" fill="currentColor" aria-hidden>
      <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0016 8c0-4.42-3.58-8-8-8z" />
    </svg>
  );
}
