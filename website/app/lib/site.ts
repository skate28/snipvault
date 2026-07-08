// Central config for the landing page. Update REPO / VERSION here only.

export const REPO = "skate28/snipvault";
export const VERSION = "v0.1.3";
export const GITHUB_URL = `https://github.com/${REPO}`;

const releaseBase = `${GITHUB_URL}/releases/latest/download`;
const rawBase = `https://raw.githubusercontent.com/${REPO}/main`;

export type Os = "windows" | "macos" | "linux";

export interface Platform {
  id: Os;
  label: string;
  binaryName: string;
  downloadUrl: string;
  installCommand: string;
  installLabel: string;
}

export const PLATFORMS: Record<Os, Platform> = {
  windows: {
    id: "windows",
    label: "Windows",
    binaryName: "snipvault-windows-x64.exe",
    downloadUrl: `${releaseBase}/snipvault-windows-x64.exe`,
    installLabel: "PowerShell",
    installCommand: `irm ${rawBase}/install.ps1 | iex`,
  },
  macos: {
    id: "macos",
    label: "macOS",
    binaryName: "snipvault-macos-arm64",
    downloadUrl: `${releaseBase}/snipvault-macos-arm64`,
    installLabel: "Terminal",
    installCommand: `curl -fsSL ${rawBase}/install.sh | sh`,
  },
  linux: {
    id: "linux",
    label: "Linux",
    binaryName: "snipvault-linux-x64",
    downloadUrl: `${releaseBase}/snipvault-linux-x64`,
    installLabel: "Terminal",
    installCommand: `curl -fsSL ${rawBase}/install.sh | sh`,
  },
};

export const PIP_COMMAND = `pip install git+${GITHUB_URL}.git`;

export const PLATFORM_ORDER: Os[] = ["windows", "macos", "linux"];

export interface Feature {
  title: string;
  body: string;
  icon: string;
}

export const FEATURES: Feature[] = [
  {
    icon: "zero",
    title: "Zero dependencies",
    body: "Pure Python standard library. Nothing to audit, nothing to break. The whole tool is a few hundred lines.",
  },
  {
    icon: "local",
    title: "Local-first storage",
    body: "Every snippet lives in a single JSON file in your home directory. No account, no server, no telemetry.",
  },
  {
    icon: "search",
    title: "Full-text search",
    body: "Search matches titles, languages, tags, and the code itself — case-insensitive, instant, offline.",
  },
  {
    icon: "tags",
    title: "Tags & languages",
    body: "Label snippets by language and freeform tags so the one command you need is always a keyword away.",
  },
  {
    icon: "pipe",
    title: "Pipe-friendly",
    body: "`show` prints raw code and nothing else, so it flows straight into your clipboard or the next command.",
  },
  {
    icon: "agent",
    title: "Agent-ready repo",
    body: "Ships AGENTS.md, portable skills, and a test subagent — built to be extended by AI coding tools.",
  },
];

export interface UsageStep {
  title: string;
  command: string;
  output: string;
}

export const USAGE: UsageStep[] = [
  {
    title: "Save a snippet",
    command: `snipvault add "recursive delete" "Remove-Item -Recurse -Force path" --lang powershell --tags files`,
    output: "added snippet 1: recursive delete",
  },
  {
    title: "List everything",
    command: "snipvault list",
    output: `  id  title                 language    tags
----------------------------------------------------
   1  recursive delete      powershell  files`,
  },
  {
    title: "Search across every field",
    command: "snipvault search files",
    output: `  id  title                 language    tags
----------------------------------------------------
   1  recursive delete      powershell  files`,
  },
  {
    title: "Pull the raw code back out",
    command: "snipvault show 1",
    output: "Remove-Item -Recurse -Force path",
  },
];
