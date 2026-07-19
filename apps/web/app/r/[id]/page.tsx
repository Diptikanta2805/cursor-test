"use client";

import { use, useEffect, useState } from "react";
import Link from "next/link";
import { getScan, type ScanResponse } from "@/lib/api";
import ResultView from "@/components/ResultView";

export default function SharedReport({
  params,
}: {
  params: Promise<{ id: string }>;
}) {
  const { id } = use(params);
  const [result, setResult] = useState<ScanResponse | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    getScan(id)
      .then(setResult)
      .catch((err) =>
        setError(err instanceof Error ? err.message : "Failed to load report"),
      );
  }, [id]);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-semibold tracking-tight">Scan report</h1>
        <Link href="/" className="text-sm text-accent hover:underline">
          New scan →
        </Link>
      </div>
      {error && (
        <div className="rounded-2xl border border-ai/40 bg-ai/10 p-4 text-sm text-ai">
          {error}
        </div>
      )}
      {!result && !error && (
        <div className="flex items-center gap-3 rounded-2xl border border-border-soft bg-surface p-6 text-sm text-muted">
          <span className="h-4 w-4 animate-spin rounded-full border-2 border-accent border-t-transparent" />
          Loading report…
        </div>
      )}
      {result && <ResultView result={result} />}
    </div>
  );
}
