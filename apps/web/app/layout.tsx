import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "VeritasAI — Open AI Text Detector",
  description:
    "Calibrated, transparent AI-generated text detection built on open RAID-benchmark-leading models.",
};

export default function RootLayout({
  children,
}: Readonly<{ children: React.ReactNode }>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} min-h-screen antialiased`}
      >
        <header className="border-b border-border-soft bg-surface/60 backdrop-blur sticky top-0 z-10">
          <div className="mx-auto flex max-w-5xl items-center justify-between px-6 py-4">
            <Link href="/" className="flex items-center gap-2">
              <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-accent-strong font-bold text-background">
                V
              </span>
              <span className="text-lg font-semibold tracking-tight">
                Veritas<span className="text-accent">AI</span>
              </span>
            </Link>
            <nav className="flex items-center gap-6 text-sm text-muted">
              <Link href="/" className="hover:text-foreground transition-colors">
                Scanner
              </Link>
              <Link
                href="/history"
                className="hover:text-foreground transition-colors"
              >
                History
              </Link>
              <Link href="/docs" className="hover:text-foreground transition-colors">
                API Docs
              </Link>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-5xl px-6 py-10">{children}</main>
        <footer className="border-t border-border-soft py-8">
          <div className="mx-auto max-w-5xl px-6 text-xs leading-relaxed text-muted">
            <p className="max-w-3xl">
              VeritasAI scores are calibrated probabilities, not proof. No
              detector is infallible — results must never be used as sole
              evidence of misconduct. Built entirely on open models and open
              benchmarks (RAID); detection signals are shown transparently for
              every scan.
            </p>
          </div>
        </footer>
      </body>
    </html>
  );
}
