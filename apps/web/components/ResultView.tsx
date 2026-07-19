"use client";

import { Fragment, useState } from "react";
import type { Boundary, ScanResponse, Sentence } from "@/lib/api";

const GENERATOR_NAMES: Record<string, string> = {
  chatgpt: "ChatGPT-class",
  gpt4: "GPT-4-class",
  gpt3: "GPT-3-class",
  gpt2: "GPT-2-class",
  "llama-chat": "Llama-class",
  "mistral-chat": "Mistral-class",
  "cohere-chat": "Cohere-class",
  "mpt-chat": "MPT-class",
};

const VERDICT_META: Record<
  string,
  { label: string; color: string; description: string }
> = {
  ai: {
    label: "Likely AI-generated",
    color: "text-ai",
    description: "The ensemble found strong AI-generation signals in this document.",
  },
  human: {
    label: "Likely human-written",
    color: "text-human",
    description: "This document reads as human-written across all signals.",
  },
  mixed: {
    label: "Mixed authorship",
    color: "text-mixed",
    description:
      "Confidently AI and confidently human regions coexist — likely AI-assisted writing.",
  },
  inconclusive: {
    label: "Inconclusive",
    color: "text-muted",
    description:
      "Signals disagree or sit near the decision boundary. We report that honestly instead of guessing.",
  },
  too_short: {
    label: "Too short to judge",
    color: "text-muted",
    description: "At least 50 words are needed for a reliable verdict.",
  },
};

function heatColor(score: number): string {
  if (score >= 0.5) {
    const alpha = 0.12 + (score - 0.5) * 0.9;
    return `rgba(248, 113, 113, ${alpha.toFixed(3)})`;
  }
  const alpha = 0.12 + (0.5 - score) * 0.55;
  return `rgba(52, 211, 153, ${alpha.toFixed(3)})`;
}

function Gauge({ probability }: { probability: number }) {
  const pct = Math.round(probability * 100);
  return (
    <div className="w-full">
      <div className="mb-1 flex justify-between text-xs text-muted">
        <span>Human</span>
        <span>AI</span>
      </div>
      <div className="relative h-3 w-full overflow-hidden rounded-full bg-surface-2">
        <div
          className="h-full rounded-full transition-all duration-700"
          style={{
            width: `${pct}%`,
            background: "linear-gradient(90deg, #34d399, #fbbf24, #f87171)",
          }}
        />
        <div
          className="absolute top-[-3px] h-[18px] w-[2px] bg-foreground"
          style={{ left: `calc(${pct}% - 1px)` }}
        />
      </div>
      <p className="mt-2 text-sm text-muted">
        <span className="font-semibold text-foreground">{pct}%</span>{" "}
        probability of AI generation
      </p>
    </div>
  );
}

function SignalRow({
  name,
  value,
  hint,
}: {
  name: string;
  value: string;
  hint: string;
}) {
  return (
    <div className="flex items-baseline justify-between gap-4 border-b border-border-soft py-2 last:border-0">
      <div>
        <p className="text-sm">{name}</p>
        <p className="text-xs text-muted">{hint}</p>
      </div>
      <span className="font-mono text-sm text-accent">{value}</span>
    </div>
  );
}

function BoundaryMarker({ boundary }: { boundary: Boundary }) {
  const toAI = boundary.direction === "human_to_ai";
  return (
    <span
      className={`mx-1 inline-flex items-center gap-1 rounded-full border px-2 py-0.5 align-middle text-[10px] font-semibold uppercase tracking-wide ${
        toAI ? "border-ai/50 bg-ai/15 text-ai" : "border-human/50 bg-human/15 text-human"
      }`}
      title={`Authorship change-point (contrast ${(boundary.contrast * 100).toFixed(0)}%)`}
    >
      {toAI ? "AI takes over →" : "→ human resumes"}
    </span>
  );
}

function HeatMap({
  sentences,
  boundaries,
}: {
  sentences: Sentence[];
  boundaries: Boundary[];
}) {
  const boundaryAt = new Map(boundaries.map((b) => [b.sentence_index, b]));
  return (
    <p className="leading-8 text-[15px]">
      {sentences.map((sentence, i) => (
        <Fragment key={i}>
          {boundaryAt.has(i) && <BoundaryMarker boundary={boundaryAt.get(i)!} />}
          <span
            title={`P(AI) = ${(sentence.score * 100).toFixed(0)}%`}
            className="rounded-sm px-0.5 transition-colors"
            style={{ backgroundColor: heatColor(sentence.score) }}
          >
            {sentence.text}{" "}
          </span>
        </Fragment>
      ))}
    </p>
  );
}

export default function ResultView({ result }: { result: ScanResponse }) {
  const [copied, setCopied] = useState(false);
  const meta = VERDICT_META[result.verdict] ?? VERDICT_META.inconclusive;
  const signals = result.signals;

  const copyShareLink = async () => {
    const url = `${window.location.origin}/r/${result.scan_id}`;
    await navigator.clipboard.writeText(url);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="space-y-6">
      <section className="rounded-2xl border border-border-soft bg-surface p-6">
        <div className="flex flex-wrap items-start justify-between gap-4">
          <div>
            <h2 className={`text-2xl font-semibold ${meta.color}`}>
              {meta.label}
            </h2>
            <p className="mt-1 max-w-xl text-sm text-muted">{meta.description}</p>
          </div>
          <button
            onClick={copyShareLink}
            className="rounded-lg border border-border-soft bg-surface-2 px-3 py-1.5 text-xs text-muted transition-colors hover:text-foreground"
          >
            {copied ? "Link copied ✓" : "Copy share link"}
          </button>
        </div>
        {result.verdict !== "too_short" && (
          <div className="mt-6">
            <Gauge probability={result.ai_probability} />
          </div>
        )}
        {result.attribution && (
          <p className="mt-4 inline-flex items-center gap-2 rounded-full border border-accent/40 bg-accent/10 px-3 py-1 text-xs text-accent">
            <span className="font-semibold">Nearest style:</span>
            {GENERATOR_NAMES[result.attribution.generator] ??
              result.attribution.generator}
            {result.attribution.share != null &&
              ` (${Math.round(result.attribution.share * 100)}% of AI neighbors)`}
          </p>
        )}
        {result.warning && (
          <p className="mt-4 rounded-lg border border-mixed/40 bg-mixed/10 p-3 text-sm text-mixed">
            {result.warning}
          </p>
        )}
        <div className="mt-4 flex flex-wrap gap-x-6 gap-y-1 text-xs text-muted">
          <span>Confidence: {result.confidence}</span>
          <span>Mode: {result.mode_used}</span>
          <span>Threshold: {result.operating_point}</span>
          <span>{result.word_count} words</span>
          <span>{result.duration_ms} ms</span>
        </div>
      </section>

      {result.sentences.length > 0 && (
        <section className="rounded-2xl border border-border-soft bg-surface p-6">
          <h3 className="mb-1 text-sm font-semibold uppercase tracking-wide text-muted">
            Sentence heat-map
          </h3>
          <p className="mb-4 text-xs text-muted">
            <span className="rounded-sm bg-ai/40 px-1">red</span> = likely AI ·{" "}
            <span className="rounded-sm bg-human/40 px-1">green</span> = likely
            human · hover a sentence for its score
            {result.boundaries.length > 0 &&
              " · markers show detected authorship change-points"}
          </p>
          <HeatMap sentences={result.sentences} boundaries={result.boundaries} />
        </section>
      )}

      <section className="rounded-2xl border border-border-soft bg-surface p-6">
        <h3 className="mb-3 text-sm font-semibold uppercase tracking-wide text-muted">
          Transparent signals
        </h3>
        {signals.fast_classifier !== undefined && (
          <SignalRow
            name="Fast classifier"
            hint="e5-small fine-tuned on the RAID benchmark (33M params)"
            value={`${(signals.fast_classifier * 100).toFixed(1)}% AI`}
          />
        )}
        {signals.deep_classifier !== undefined && (
          <SignalRow
            name="Deep classifier"
            hint="DeBERTa-v3-large detector (RAID leaderboard leader)"
            value={`${(signals.deep_classifier * 100).toFixed(1)}% AI`}
          />
        )}
        {signals.style_retrieval !== undefined && (
          <SignalRow
            name="Style retrieval"
            hint="kNN vote over a reference index of human & LLM writing styles (DeTeCtive-style)"
            value={`${(signals.style_retrieval * 100).toFixed(1)}% AI`}
          />
        )}
        {signals.step_uniformity != null && (
          <SignalRow
            name="Trajectory uniformity"
            hint="Regularity of semantic transitions between text windows (GTCL-inspired, informational)"
            value={signals.step_uniformity.toFixed(3)}
          />
        )}
        {signals.perplexity != null && (
          <SignalRow
            name="Perplexity"
            hint="How predictable the text is to a language model — AI text is usually low"
            value={signals.perplexity.toFixed(1)}
          />
        )}
        {signals.burstiness != null && (
          <SignalRow
            name="Burstiness"
            hint="Variation in sentence-level perplexity — human writing is burstier"
            value={signals.burstiness.toFixed(2)}
          />
        )}
        {signals.statistical_likelihood != null && (
          <SignalRow
            name="Statistical arm"
            hint="Perplexity + burstiness mapped to an AI likelihood (weak prior in the ensemble)"
            value={`${(signals.statistical_likelihood * 100).toFixed(1)}% AI`}
          />
        )}
      </section>
    </div>
  );
}
