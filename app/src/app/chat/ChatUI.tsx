"use client";
import { useState, useRef, useEffect } from "react";
import Link from "next/link";
import type { Route } from "next";

type Msg = {
  role: "user" | "assistant";
  content: string;
  sources?: Array<{ index: number; title: string; path: string }>;
};

export default function ChatUI() {
  const [messages, setMessages] = useState<Msg[]>([]);
  const [input, setInput] = useState("");
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const bottomRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, pending]);

  async function send() {
    const query = input.trim();
    if (!query || pending) return;
    setInput("");
    setError(null);
    const history = messages.map((m) => ({ role: m.role, content: m.content }));
    const userMsg: Msg = { role: "user", content: query };
    setMessages((m) => [...m, userMsg]);
    setPending(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ query, history }),
      });
      const data = await res.json();
      if (!res.ok) {
        setError(data.error ?? `HTTP ${res.status}`);
      } else {
        setMessages((m) => [
          ...m,
          { role: "assistant", content: data.answer, sources: data.sources },
        ]);
      }
    } catch (e) {
      setError(e instanceof Error ? e.message : "Request failed");
    } finally {
      setPending(false);
    }
  }

  return (
    <div className="mt-6">
      <div className="space-y-4 min-h-[200px]">
        {messages.length === 0 && !pending && (
          <div className="rounded-md border border-dashed border-stone-300 p-6 text-sm text-stone-500">
            Example questions:
            <ul className="mt-2 space-y-1">
              <li>— What is Anthropic&rsquo;s contextual retrieval and what numbers does it report?</li>
              <li>— Compare v0, Lovable, Bolt, and Replit at the architectural level.</li>
              <li>— What makes outbound emails land in the inbox in 2026?</li>
            </ul>
          </div>
        )}
        {messages.map((m, i) => (
          <MessageBubble key={i} msg={m} />
        ))}
        {pending && (
          <div className="rounded-md bg-white border border-stone-200 p-4 text-sm text-stone-500">
            Searching vault and asking Claude…
          </div>
        )}
        {error && (
          <div className="rounded-md bg-red-50 border border-red-200 p-4 text-sm text-red-700">
            {error}
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      <form
        onSubmit={(e) => {
          e.preventDefault();
          void send();
        }}
        className="mt-6 flex gap-2"
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask the vault…"
          disabled={pending}
          className="flex-1 rounded-md border border-stone-300 bg-white px-4 py-3 text-base outline-none focus:border-accent disabled:opacity-50"
          autoFocus
        />
        <button
          type="submit"
          disabled={pending || !input.trim()}
          className="rounded-md bg-accent px-5 py-3 text-sm font-medium text-white hover:bg-amber-700 disabled:opacity-50 transition"
        >
          {pending ? "…" : "Ask"}
        </button>
      </form>
    </div>
  );
}

function MessageBubble({ msg }: { msg: Msg }) {
  if (msg.role === "user") {
    return (
      <div className="rounded-md bg-stone-100 p-4 text-sm">
        <div className="text-xs uppercase tracking-wider text-stone-500 mb-1">You</div>
        <div className="whitespace-pre-wrap">{msg.content}</div>
      </div>
    );
  }
  return (
    <div className="rounded-md bg-white border border-stone-200 p-4 text-sm">
      <div className="text-xs uppercase tracking-wider text-stone-500 mb-1">Claude</div>
      <div className="whitespace-pre-wrap leading-relaxed">{msg.content}</div>
      {msg.sources && msg.sources.length > 0 && (
        <div className="mt-4 pt-3 border-t border-stone-100">
          <div className="text-xs uppercase tracking-wider text-stone-500 mb-2">Sources</div>
          <ol className="space-y-1">
            {msg.sources.map((s) => (
              <li key={s.index} className="text-xs">
                <span className="text-stone-400 mr-2">[{s.index}]</span>
                <Link
                  href={`/vault/${s.path}` as Route}
                  className="text-accent hover:underline"
                >
                  {s.title}
                </Link>
              </li>
            ))}
          </ol>
        </div>
      )}
    </div>
  );
}
