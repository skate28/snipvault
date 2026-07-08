import type { Metadata } from "next";
import { Nav } from "../components/Nav";
import { Footer } from "../components/Footer";
import { GITHUB_URL } from "../lib/site";
import { getReleases, statusOf, type Status } from "../lib/releases";

export const metadata: Metadata = {
  title: "Releases — Snippet Vault",
  description:
    "Every released version of Snippet Vault with its release date, stability, and downloads for Windows, macOS, and Linux.",
};

// Regenerate this page at most once an hour so new releases show up on their own.
export const revalidate = 3600;

const OS_LABEL: Record<string, string> = {
  windows: "Windows",
  macos: "macOS",
  linux: "Linux",
};

const STATUS_STYLE: Record<Status, { label: string; className: string }> = {
  latest: { label: "Latest", className: "border-accent text-accent" },
  stable: { label: "Stable", className: "border-term-green text-term-green" },
  development: {
    label: "Development",
    className: "border-term-yellow text-term-yellow",
  },
  prerelease: { label: "Pre-release", className: "border-border-bright text-fg-faint" },
};

function formatDate(iso: string): string {
  return new Intl.DateTimeFormat("en-US", {
    year: "numeric",
    month: "short",
    day: "numeric",
  }).format(new Date(iso));
}

export default async function VersionsPage() {
  const releases = await getReleases();

  return (
    <>
      <Nav />
      <main className="flex-1">
        <section className="mx-auto max-w-5xl px-5 py-16">
          <div className="mb-10">
            <p className="mb-3 font-mono text-xs uppercase tracking-[0.2em] text-accent">
              Releases
            </p>
            <h1 className="text-3xl font-bold tracking-tight sm:text-4xl">
              Every version
            </h1>
            <p className="mt-4 max-w-2xl text-fg-dim">
              Every release, newest first, with its date, stability, and downloads.
              Pre-1.0 (0.x) versions are marked <em>Development</em> — the tool works,
              but commands may still change before <span className="font-mono">1.0.0</span>.
            </p>
          </div>

          {releases.length === 0 ? (
            <div className="rounded-xl border border-border bg-bg-card p-8 text-center text-fg-dim">
              Couldn&apos;t load releases right now.{" "}
              <a
                href={`${GITHUB_URL}/releases`}
                target="_blank"
                rel="noreferrer"
                className="text-accent underline-offset-4 hover:underline"
              >
                View them on GitHub
              </a>
              .
            </div>
          ) : (
            <div className="overflow-x-auto rounded-xl border border-border">
              <table className="w-full min-w-[640px] border-collapse text-sm">
                <thead>
                  <tr className="border-b border-border bg-bg-elev text-left text-fg-faint">
                    <th className="px-4 py-3 font-medium">Version</th>
                    <th className="px-4 py-3 font-medium">Released</th>
                    <th className="px-4 py-3 font-medium">Status</th>
                    <th className="px-4 py-3 font-medium">Downloads</th>
                    <th className="px-4 py-3 font-medium">Notes</th>
                  </tr>
                </thead>
                <tbody>
                  {releases.map((r, i) => {
                    // The newest non-prerelease is the "latest".
                    const isLatest =
                      !r.prerelease &&
                      releases.findIndex((x) => !x.prerelease) === i;
                    const status = STATUS_STYLE[statusOf(r, isLatest)];
                    const downloads = r.assets.filter((a) => a.os !== "other");
                    return (
                      <tr
                        key={r.tag}
                        className="border-b border-border/60 last:border-0 hover:bg-bg-card/60"
                      >
                        <td className="px-4 py-3 font-mono font-medium text-fg">
                          {r.tag}
                        </td>
                        <td className="px-4 py-3 text-fg-dim">{formatDate(r.date)}</td>
                        <td className="px-4 py-3">
                          <span
                            className={`inline-flex rounded-full border px-2.5 py-0.5 text-xs font-medium ${status.className}`}
                          >
                            {status.label}
                          </span>
                        </td>
                        <td className="px-4 py-3">
                          <div className="flex flex-wrap gap-x-3 gap-y-1">
                            {downloads.length === 0 ? (
                              <span className="text-fg-faint">—</span>
                            ) : (
                              downloads.map((a) => (
                                <a
                                  key={a.name}
                                  href={a.url}
                                  className="text-accent underline-offset-4 hover:underline"
                                >
                                  {OS_LABEL[a.os]}
                                </a>
                              ))
                            )}
                          </div>
                        </td>
                        <td className="px-4 py-3">
                          <a
                            href={r.notesUrl}
                            target="_blank"
                            rel="noreferrer"
                            className="text-fg-dim underline-offset-4 hover:text-fg hover:underline"
                          >
                            Notes ↗
                          </a>
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          )}
        </section>
      </main>
      <Footer />
    </>
  );
}
