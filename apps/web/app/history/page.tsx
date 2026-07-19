"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { getHistory, type ScanSummary } from "@/lib/api";

const VERDICT_COLORS: Record<string, string> = {
  ai: "text-ai border-ai/40 bg-ai/10",
  human: "text-human border-human/40 bg-human/10",
  mixed: "text-mixed border-mixed/40 bg-mixed/10",
  inconclusive: "text-muted border-border-soft bg-surface-2",
  too_short: "text-muted border-border-soft bg-surface-2",
};

export default function HistoryPage() {
  const [scans, setScans] = useState<ScanSummary[] | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getHistory()
      .then(setScans)
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Failed to load history"),
      );
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-semibold tracking-tight">Scan history</h1>
      <p className="text-sm text-muted">
        Recent scans from this device (or API key).
      </p>
      {error && (
        <div className="rounded-2xl border border-ai/40 bg-ai/10 p-4 text-sm text-ai">
          {error}
        </div>
      )}
      {scans && scans.length === 0 && (
        <div className="rounded-2xl border border-border-soft bg-surface p-8 text-center text-sm text-muted">
          No scans yet.{" "}
          <Link href="/" className="text-accent hover:underline">
            Run your first scan →
          </Link>
        </div>
      )}
      <div className="space-y-3">
        {scans?.map((scan) => (
          <Link
            key={scan.scan_id}
            href={`/r/${scan.scan_id}`}
            className="block rounded-2xl border border-border-soft bg-surface p-4 transition-colors hover:border-accent/50"
          >
            <div className="flex items-center justify-between gap-4">
              <span
                className={`rounded-full border px-2.5 py-0.5 text-xs font-medium capitalize ${
                  VERDICT_COLORS[scan.verdict] ?? VERDICT_COLORS.inconclusive
                }`}
              >
                {scan.verdict.replace("_", " ")}
              </span>
              <span className="text-xs text-muted">
                {new Date(scan.created_at).toLocaleString()} ·{" "}
                {scan.word_count} words ·{" "}
                {Math.round(scan.ai_probability * 100)}% AI
              </span>
            </div>
            <p className="mt-2 truncate text-sm text-muted">
              {scan.text_preview}
            </p>
          </Link>
        ))}
      </div>
    </div>
  );
}
