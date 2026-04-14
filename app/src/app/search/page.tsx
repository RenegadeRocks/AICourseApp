"use client";
import { useEffect, useState } from "react";
import Link from "next/link";

type Hit = { id: string; title: string; path: string; field: string };

export default function SearchPage() {
  const [q, setQ] = useState("");
  const [hits, setHits] = useState<Hit[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const t = setTimeout(() => {
      if (!q.trim()) {
        setHits([]);
        return;
      }
      setLoading(true);
      fetch(`/api/search?q=${encodeURIComponent(q)}`)
        .then((r) => r.json())
        .then((d: { hits: Hit[] }) => setHits(d.hits))
        .finally(() => setLoading(false));
    }, 150);
    return () => clearTimeout(t);
  }, [q]);

  return (
    <div className="max-w-3xl">
      <h1 className="text-3xl font-bold tracking-tight">Search</h1>
      <input
        autoFocus
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Search the vault…"
        className="mt-6 w-full rounded-md border border-stone-300 bg-white px-4 py-3 text-lg outline-none focus:border-accent"
      />
      <div className="mt-6 text-sm text-stone-500">
        {loading ? "Searching…" : hits.length > 0 ? `${hits.length} results` : q ? "No results" : "Start typing."}
      </div>
      <ul className="mt-4 divide-y divide-stone-100 rounded border border-stone-200 bg-white">
        {hits.map((h) => (
          <li key={h.id}>
            <Link href={`/vault/${h.path}`} className="block px-4 py-3 hover:bg-stone-50">
              <div className="font-medium">{h.title}</div>
              <div className="text-xs text-stone-500">{h.path}</div>
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
