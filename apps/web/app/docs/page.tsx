import { API_URL } from "@/lib/api";

const CURL_EXAMPLE = `curl -X POST ${API_URL}/v1/scan \\
  -H "Content-Type: application/json" \\
  -H "X-API-Key: vk_your_key" \\
  -d '{
    "text": "Your document text here (at least 50 words)…",
    "mode": "deep",
    "operating_point": "strict"
  }'`;

const RESPONSE_EXAMPLE = `{
  "scan_id": "1f3a…",
  "verdict": "ai",              // human | ai | mixed | inconclusive | too_short
  "ai_probability": 0.94,
  "confidence": "high",
  "operating_point": "strict",  // conformally calibrated: FPR ≤ 1% (strict) / 5% (balanced)
  "mode_used": "deep",
  "sentences": [{ "text": "…", "start": 0, "end": 42, "score": 0.97 }],
  "attribution": { "generator": "chatgpt", "share": 0.8 },
  "boundaries": [
    { "sentence_index": 7, "direction": "human_to_ai", "contrast": 0.62 }
  ],
  "signals": {
    "fast_classifier": 0.95,
    "deep_classifier": 0.93,
    "style_retrieval": 0.88,
    "step_uniformity": 0.983,
    "perplexity": 14.2,
    "burstiness": 0.31
  }
}`;

const ENDPOINTS: Array<[string, string, string]> = [
  ["POST", "/v1/scan", "Scan raw text. Body: { text, mode, operating_point }"],
  ["POST", "/v1/scan/file", "Scan an uploaded PDF, DOCX, TXT, or MD file (multipart)"],
  ["POST", "/v1/scan/batch", "Scan up to 20 documents in one request"],
  ["GET", "/v1/scan/{id}", "Retrieve a previous scan (also powers share links)"],
  ["GET", "/v1/history", "Recent scans for the caller"],
  ["GET", "/v1/usage", "Today's quota usage"],
  ["GET", "/v1/health", "Service and model status"],
];

export default function DocsPage() {
  return (
    <div className="space-y-8">
      <section className="space-y-3">
        <h1 className="text-2xl font-semibold tracking-tight">API documentation</h1>
        <p className="max-w-2xl text-sm leading-6 text-muted">
          The full interactive OpenAPI reference lives at{" "}
          <a
            href={`${API_URL}/docs`}
            className="text-accent hover:underline"
            target="_blank"
            rel="noreferrer"
          >
            {API_URL}/docs
          </a>
          . Anonymous callers get a small daily quota; pass an{" "}
          <code className="rounded bg-surface-2 px-1.5 py-0.5 font-mono text-xs">
            X-API-Key
          </code>{" "}
          header for higher limits.
        </p>
      </section>

      <section className="rounded-2xl border border-border-soft bg-surface p-6">
        <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-muted">
          Endpoints
        </h2>
        <div className="space-y-2">
          {ENDPOINTS.map(([method, path, description]) => (
            <div
              key={method + path}
              className="flex flex-wrap items-baseline gap-3 border-b border-border-soft py-2 text-sm last:border-0"
            >
              <span className="w-12 font-mono text-xs font-bold text-accent">
                {method}
              </span>
              <code className="font-mono text-foreground">{path}</code>
              <span className="text-xs text-muted">{description}</span>
            </div>
          ))}
        </div>
      </section>

      <section className="rounded-2xl border border-border-soft bg-surface p-6">
        <h2 className="mb-4 text-sm font-semibold uppercase tracking-wide text-muted">
          Example request
        </h2>
        <pre className="overflow-x-auto rounded-xl bg-surface-2 p-4 font-mono text-xs leading-6">
          {CURL_EXAMPLE}
        </pre>
        <h2 className="mb-4 mt-6 text-sm font-semibold uppercase tracking-wide text-muted">
          Example response
        </h2>
        <pre className="overflow-x-auto rounded-xl bg-surface-2 p-4 font-mono text-xs leading-6">
          {RESPONSE_EXAMPLE}
        </pre>
      </section>

      <section className="rounded-2xl border border-border-soft bg-surface p-6 text-sm leading-6 text-muted">
        <h2 className="mb-2 text-sm font-semibold uppercase tracking-wide">
          Responsible use
        </h2>
        <p>
          Verdicts are calibrated probabilities, not proof. The strict
          operating point targets a 1% false-positive rate and should be used
          for any high-stakes decision. Never treat a detector score as sole
          evidence of misconduct, and be aware that detectors have documented
          higher false-positive rates on non-native English writing.
        </p>
      </section>
    </div>
  );
}
