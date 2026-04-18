import type { Metadata } from "next";
import Link from "next/link";
import "./globals.css";

export const metadata: Metadata = {
  title: "AI Pro-level Course",
  description: "Personal daily study for the AI Pro-level Course",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className="min-h-screen">
        <header className="border-b border-stone-200 bg-paper/80 backdrop-blur sticky top-0 z-10">
          <div className="mx-auto max-w-6xl px-6 h-14 flex items-center justify-between">
            <Link href="/" className="font-semibold tracking-tight">
              AI Pro-level Course
            </Link>
            <nav className="flex gap-6 text-sm text-stone-600">
              <Link href="/" className="hover:text-ink">Today</Link>
              <Link href="/schedule" className="hover:text-ink">Schedule</Link>
              <Link href="/vault/00-program/index" className="hover:text-ink">Program</Link>
              <Link href="/search" className="hover:text-ink">Search</Link>
              <Link href="/chat" className="hover:text-ink">Chat</Link>
              <Link href="/progress" className="hover:text-ink">Progress</Link>
              <Link href="/exports" className="hover:text-ink">Exports</Link>
            </nav>
          </div>
        </header>
        <main className="mx-auto max-w-6xl px-6 py-10">{children}</main>
        <footer className="border-t border-stone-200 mt-16 py-8 text-center text-xs text-stone-500">
          Built for deep daily study. Content lives in <code>vault/</code>.
        </footer>
      </body>
    </html>
  );
}
