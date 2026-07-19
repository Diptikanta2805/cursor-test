import Scanner from "@/components/Scanner";

export default function Home() {
  return (
    <div className="space-y-8">
      <section className="space-y-3">
        <h1 className="text-3xl font-semibold tracking-tight">
          Is this text <span className="text-accent">AI-generated?</span>
        </h1>
        <p className="max-w-2xl text-sm leading-6 text-muted">
          VeritasAI runs an ensemble of open, RAID-benchmark-leading detectors
          with GPTZero-style perplexity and burstiness signals — and shows you
          every component score. Pick <em>strict</em> mode to minimize false
          accusations, or <em>deep scan</em> for the most accurate verdict.
        </p>
      </section>
      <Scanner />
    </div>
  );
}
