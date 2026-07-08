export function Logo({ className }: { className?: string }) {
  return (
    <svg viewBox="0 0 32 32" fill="none" className={className} aria-hidden>
      <rect
        x="2.5"
        y="2.5"
        width="27"
        height="27"
        rx="7"
        fill="#0e1016"
        stroke="url(#lg)"
        strokeWidth="1.5"
      />
      <path
        d="M11 12l3.2 4L11 20"
        stroke="#2dd4bf"
        strokeWidth="2"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
      <path d="M17 20.5h5" stroke="#5eead4" strokeWidth="2" strokeLinecap="round" />
      <defs>
        <linearGradient id="lg" x1="2" y1="2" x2="30" y2="30" gradientUnits="userSpaceOnUse">
          <stop stopColor="#2dd4bf" />
          <stop offset="1" stopColor="#1e2230" />
        </linearGradient>
      </defs>
    </svg>
  );
}
