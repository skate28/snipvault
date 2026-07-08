import { InstallTabs } from "./InstallTabs";

export function Install() {
  return (
    <section
      id="install"
      className="relative mx-auto max-w-6xl scroll-mt-20 px-5 py-24"
    >
      <div className="mb-14 text-center">
        <p className="mb-3 font-mono text-xs uppercase tracking-[0.2em] text-accent">
          Install
        </p>
        <h2 className="text-3xl font-bold tracking-tight sm:text-4xl">
          Up and running in seconds
        </h2>
        <p className="mx-auto mt-4 max-w-xl text-fg-dim">
          Pick your platform. Paste one line, or grab the binary directly — no
          package manager, no dependencies.
        </p>
      </div>

      <InstallTabs />
    </section>
  );
}
