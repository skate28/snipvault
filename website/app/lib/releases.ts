// Fetches published releases from the GitHub API so the /versions page always
// reflects reality — every tag you push shows up automatically, no edits needed.

import { REPO } from "./site";

export interface ReleaseAsset {
  name: string;
  url: string;
  os: "windows" | "macos" | "linux" | "other";
}

export interface Release {
  tag: string;
  date: string; // ISO
  prerelease: boolean;
  notesUrl: string;
  assets: ReleaseAsset[];
}

export type Status = "latest" | "stable" | "development" | "prerelease";

function osOf(name: string): ReleaseAsset["os"] {
  const n = name.toLowerCase();
  if (n.includes("windows")) return "windows";
  if (n.includes("macos") || n.includes("darwin")) return "macos";
  if (n.includes("linux")) return "linux";
  return "other";
}

// Classify a release's stability. Pre-1.0 (0.x) is "development" per semver;
// 1.0.0+ is "stable". The newest non-prerelease is additionally the "latest".
export function statusOf(release: Release, isLatest: boolean): Status {
  if (release.prerelease) return "prerelease";
  if (isLatest) return "latest";
  const major = parseInt(release.tag.replace(/^v/, "").split(".")[0], 10);
  return major >= 1 ? "stable" : "development";
}

export async function getReleases(): Promise<Release[]> {
  try {
    const res = await fetch(
      `https://api.github.com/repos/${REPO}/releases?per_page=100`,
      {
        headers: { Accept: "application/vnd.github+json" },
        next: { revalidate: 3600 }, // refresh at most once an hour
      },
    );
    if (!res.ok) return [];
    const data = (await res.json()) as Array<{
      tag_name: string;
      draft: boolean;
      prerelease: boolean;
      published_at: string;
      html_url: string;
      assets: Array<{ name: string; browser_download_url: string }>;
    }>;
    return data
      .filter((r) => !r.draft)
      .map((r) => ({
        tag: r.tag_name,
        date: r.published_at,
        prerelease: r.prerelease,
        notesUrl: r.html_url,
        assets: r.assets.map((a) => ({
          name: a.name,
          url: a.browser_download_url,
          os: osOf(a.name),
        })),
      }));
  } catch {
    return [];
  }
}
