const paths: Record<string, React.ReactNode> = {
  zero: <path d="M12 3a9 9 0 100 18 9 9 0 000-18zm0 0l0 18" />,
  local: (
    <>
      <path d="M4 7l8-4 8 4v10l-8 4-8-4V7z" />
      <path d="M4 7l8 4 8-4M12 11v10" />
    </>
  ),
  search: (
    <>
      <circle cx="11" cy="11" r="6" />
      <path d="M20 20l-4-4" />
    </>
  ),
  tags: (
    <>
      <path d="M3 7v5l8 8 6-6-8-8H3z" />
      <circle cx="7" cy="11" r="1.2" fill="currentColor" stroke="none" />
    </>
  ),
  pipe: <path d="M4 8h10a4 4 0 010 8H8m0 0l3-3m-3 3l3 3" />,
  agent: (
    <>
      <rect x="5" y="8" width="14" height="10" rx="2" />
      <path d="M12 8V4M9 13h.01M15 13h.01" />
    </>
  ),
};

export function FeatureIcon({ name }: { name: string }) {
  return (
    <svg
      width="22"
      height="22"
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.6"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden
    >
      {paths[name] ?? paths.zero}
    </svg>
  );
}
