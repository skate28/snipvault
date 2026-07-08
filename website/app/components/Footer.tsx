import { GITHUB_URL, VERSION } from "../lib/site";
import { Logo } from "./Logo";

export function Footer() {
  return (
    <footer className="mt-auto border-t border-border/60">
      <div className="mx-auto flex max-w-6xl flex-col items-center justify-between gap-6 px-5 py-10 sm:flex-row">
        <div className="flex items-center gap-2.5 text-sm text-fg-dim">
          <Logo className="h-6 w-6" />
          <span className="font-medium text-fg">Snippet Vault</span>
          <span className="font-mono text-xs text-fg-faint">{VERSION}</span>
        </div>
        <div className="flex flex-wrap items-center justify-center gap-x-6 gap-y-2 text-sm text-fg-dim">
          <a href={GITHUB_URL} target="_blank" rel="noreferrer" className="transition hover:text-fg">
            GitHub
          </a>
          <a
            href={`${GITHUB_URL}/blob/main/README.md`}
            target="_blank"
            rel="noreferrer"
            className="transition hover:text-fg"
          >
            README
          </a>
          <a
            href={`${GITHUB_URL}/blob/main/snipvault-docs.md`}
            target="_blank"
            rel="noreferrer"
            className="transition hover:text-fg"
          >
            Docs
          </a>
          <a
            href={`${GITHUB_URL}/releases`}
            target="_blank"
            rel="noreferrer"
            className="transition hover:text-fg"
          >
            Releases
          </a>
          <span className="text-fg-faint">MIT License</span>
        </div>
      </div>
    </footer>
  );
}
