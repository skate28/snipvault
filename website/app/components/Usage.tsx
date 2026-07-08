import { USAGE } from "../lib/site";

export function Usage() {
  return (
    <section id="usage" className="mx-auto max-w-4xl scroll-mt-20 px-5 py-24">
      <div className="mb-14 text-center">
        <p className="mb-3 font-mono text-xs uppercase tracking-[0.2em] text-accent">
          The whole workflow
        </p>
        <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
          Five commands. That&apos;s it.
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-fg-dim">
          Save what you learn, find it when you need it, pipe it back out.
        </p>
      </div>

      <div className="space-y-5">
        {USAGE.map((step, i) => (
          <div
            key={step.title}
            className="overflow-hidden rounded-xl border border-border bg-[#0b0d13]"
          >
            <div className="flex items-center gap-3 border-b border-border px-4 py-2.5">
              <span className="font-mono text-xs text-fg-faint">
                {String(i + 1).padStart(2, "0")}
              </span>
              <span className="text-sm font-medium text-fg-dim">{step.title}</span>
            </div>
            <div className="overflow-x-auto p-4 font-mono text-[13px] leading-relaxed">
              <div className="whitespace-nowrap">
                <span className="mr-2 select-none text-accent">$</span>
                <span className="text-fg">{step.command}</span>
              </div>
              <pre className="mt-1.5 whitespace-pre text-fg-dim">{step.output}</pre>
            </div>
          </div>
        ))}
      </div>
    </section>
  );
}
