"use client";

import { useRef, useState } from "react";
import { scanFile, scanText, type ScanResponse } from "@/lib/api";
import ResultView from "@/components/ResultView";

const SAMPLE_TEXT = `Artificial intelligence has fundamentally transformed the landscape of modern technology, offering unprecedented opportunities for innovation across diverse industries. From healthcare to finance, organizations are leveraging machine learning algorithms to streamline operations, enhance decision-making processes, and deliver personalized experiences to their customers. As these technologies continue to evolve, it is essential for businesses to adopt a strategic approach to implementation, ensuring that ethical considerations and data privacy remain at the forefront of their initiatives.`;

export default function Scanner() {
  const [text, setText] = useState("");
  const [mode, setMode] = useState<"fast" | "deep">("fast");
  const [operatingPoint, setOperatingPoint] = useState<"balanced" | "strict">(
    "balanced",
  );
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<ScanResponse | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);

  const wordCount = text.trim() ? text.trim().split(/\s+/).length : 0;

  const runScan = async () => {
    if (!text.trim() || loading) return;
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      setResult(await scanText(text, mode, operatingPoint));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Scan failed");
    } finally {
      setLoading(false);
    }
  };

  const runFileScan = async (file: File) => {
    setLoading(true);
    setError(null);
    setResult(null);
    try {
      setResult(await scanFile(file, mode, operatingPoint));
      setText(`(uploaded file: ${file.name})`);
    } catch (err) {
      setError(err instanceof Error ? err.message : "File scan failed");
    } finally {
      setLoading(false);
      if (fileInput.current) fileInput.current.value = "";
    }
  };

  return (
    <div className="space-y-6">
      <section className="rounded-2xl border border-border-soft bg-surface p-6">
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          placeholder="Paste at least 50 words of text to analyze…"
          rows={9}
          className="w-full resize-y rounded-xl border border-border-soft bg-surface-2 p-4 text-[15px] leading-7 outline-none transition-colors placeholder:text-muted focus:border-accent"
          data-testid="scan-input"
        />
        <div className="mt-4 flex flex-wrap items-center gap-3">
          <button
            onClick={runScan}
            disabled={loading || wordCount === 0}
            className="rounded-xl bg-accent-strong px-6 py-2.5 font-semibold text-background transition-opacity hover:opacity-90 disabled:opacity-40"
            data-testid="scan-button"
          >
            {loading ? "Scanning…" : "Scan text"}
          </button>

          <button
            onClick={() => fileInput.current?.click()}
            disabled={loading}
            className="rounded-xl border border-border-soft bg-surface-2 px-4 py-2.5 text-sm text-muted transition-colors hover:text-foreground disabled:opacity-40"
          >
            Upload PDF / DOCX / TXT
          </button>
          <input
            ref={fileInput}
            type="file"
            accept=".pdf,.docx,.txt,.md"
            className="hidden"
            onChange={(e) => {
              const file = e.target.files?.[0];
              if (file) void runFileScan(file);
            }}
          />

          <div className="ml-auto flex items-center gap-3 text-xs">
            <div className="flex overflow-hidden rounded-lg border border-border-soft">
              {(["fast", "deep"] as const).map((m) => (
                <button
                  key={m}
                  onClick={() => setMode(m)}
                  className={`px-3 py-1.5 capitalize transition-colors ${
                    mode === m
                      ? "bg-accent-strong text-background"
                      : "bg-surface-2 text-muted hover:text-foreground"
                  }`}
                >
                  {m === "fast" ? "Fast scan" : "Deep scan"}
                </button>
              ))}
            </div>
            <div className="flex overflow-hidden rounded-lg border border-border-soft">
              {(["balanced", "strict"] as const).map((op) => (
                <button
                  key={op}
                  onClick={() => setOperatingPoint(op)}
                  title={
                    op === "strict"
                      ? "Fewer false accusations (target 1% FPR)"
                      : "Balanced threshold (target 5% FPR)"
                  }
                  className={`px-3 py-1.5 capitalize transition-colors ${
                    operatingPoint === op
                      ? "bg-accent-strong text-background"
                      : "bg-surface-2 text-muted hover:text-foreground"
                  }`}
                >
                  {op}
                </button>
              ))}
            </div>
          </div>
        </div>
        <div className="mt-3 flex items-center justify-between text-xs text-muted">
          <span>{wordCount} words {wordCount > 0 && wordCount < 50 && "· need ≥ 50 for a verdict"}</span>
          <button
            onClick={() => setText(SAMPLE_TEXT)}
            className="underline decoration-dotted hover:text-foreground"
          >
            Try a sample
          </button>
        </div>
      </section>

      {loading && (
        <div className="flex items-center gap-3 rounded-2xl border border-border-soft bg-surface p-6 text-sm text-muted">
          <span className="h-4 w-4 animate-spin rounded-full border-2 border-accent border-t-transparent" />
          Running the detection ensemble{mode === "deep" && " (deep scan: DeBERTa + Binoculars + RAIDAR rewrite)"}…
        </div>
      )}

      {error && (
        <div className="rounded-2xl border border-ai/40 bg-ai/10 p-4 text-sm text-ai">
          {error}
        </div>
      )}

      {result && <ResultView result={result} />}
    </div>
  );
}
