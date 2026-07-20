export const API_URL =
  process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8000";

export type Sentence = {
  text: string;
  start: number;
  end: number;
  score: number;
};

export type Signals = {
  fast_classifier?: number;
  deep_classifier?: number;
  style_retrieval?: number;
  neighbor_similarity?: number;
  binoculars_score?: number;
  binoculars_likelihood?: number | null;
  rewrite_similarity?: number | null;
  raidar_likelihood?: number | null;
  step_similarity_mean?: number | null;
  step_uniformity?: number | null;
  perplexity?: number | null;
  mean_sentence_perplexity?: number | null;
  burstiness?: number | null;
  statistical_likelihood?: number | null;
};

export type Attribution = {
  generator: string;
  share: number | null;
};

export type Boundary = {
  sentence_index: number;
  direction: "human_to_ai" | "ai_to_human";
  contrast: number;
};

export type ScanResponse = {
  scan_id: string;
  created_at: string;
  verdict: "human" | "ai" | "mixed" | "inconclusive" | "too_short";
  ai_probability: number;
  confidence: "high" | "medium" | "low";
  operating_point: "strict" | "balanced";
  mode_used: "fast" | "deep";
  word_count: number;
  duration_ms: number;
  warning: string | null;
  sentences: Sentence[];
  signals: Signals;
  attribution: Attribution | null;
  boundaries: Boundary[];
  model_version: string;
};

export type ScanSummary = {
  scan_id: string;
  created_at: string;
  verdict: ScanResponse["verdict"];
  ai_probability: number;
  word_count: number;
  text_preview: string;
};

async function handle<T>(response: Response): Promise<T> {
  if (!response.ok) {
    let detail = `Request failed (${response.status})`;
    try {
      const body = await response.json();
      if (typeof body.detail === "string") detail = body.detail;
    } catch {
      // keep default message
    }
    throw new Error(detail);
  }
  return response.json() as Promise<T>;
}

export async function scanText(
  text: string,
  mode: "fast" | "deep",
  operatingPoint: "strict" | "balanced",
): Promise<ScanResponse> {
  const response = await fetch(`${API_URL}/v1/scan`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ text, mode, operating_point: operatingPoint }),
  });
  return handle<ScanResponse>(response);
}

export async function scanFile(
  file: File,
  mode: "fast" | "deep",
  operatingPoint: "strict" | "balanced",
): Promise<ScanResponse> {
  const form = new FormData();
  form.append("file", file);
  form.append("mode", mode);
  form.append("operating_point", operatingPoint);
  const response = await fetch(`${API_URL}/v1/scan/file`, {
    method: "POST",
    body: form,
  });
  return handle<ScanResponse>(response);
}

export async function getScan(scanId: string): Promise<ScanResponse> {
  const response = await fetch(`${API_URL}/v1/scan/${scanId}`);
  return handle<ScanResponse>(response);
}

export async function getHistory(): Promise<ScanSummary[]> {
  const response = await fetch(`${API_URL}/v1/history`);
  return handle<ScanSummary[]>(response);
}
