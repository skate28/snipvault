import { FEATURES } from "../lib/site";
import { FeatureIcon } from "./FeatureIcon";

export function Features() {
  return (
    <section id="features" className="mx-auto max-w-6xl scroll-mt-20 px-5 py-24">
      <div className="mb-14 text-center">
        <p className="mb-3 font-mono text-xs uppercase tracking-[0.2em] text-accent">
          Why Snippet Vault
        </p>
        <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
          Small tool. No lock-in.
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-fg-dim">
          Everything runs locally, ships in a single file, and gets out of your way.
        </p>
      </div>

      <div className="grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
        {FEATURES.map((f) => (
          <div
            key={f.title}
            className="group rounded-2xl border border-border bg-bg-card p-6 transition hover:border-border-bright"
          >
            <div className="mb-4 inline-flex h-11 w-11 items-center justify-center rounded-xl border border-border-bright bg-bg-elev text-accent transition group-hover:border-accent">
              <FeatureIcon name={f.icon} />
            </div>
            <h3 className="mb-1.5 font-semibold text-fg">{f.title}</h3>
            <p className="text-sm leading-relaxed text-fg-dim">{f.body}</p>
          </div>
        ))}
      </div>
    </section>
  );
}
