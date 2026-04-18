import ChatUI from "./ChatUI";

export default function ChatPage() {
  return (
    <div className="max-w-3xl">
      <h1 className="text-3xl font-bold tracking-tight">Chat with the vault</h1>
      <p className="mt-2 text-stone-600 text-sm">
        Ask questions grounded in the shipped lessons. Uses retrieval over the
        full vault + Claude Sonnet 4.6 to answer with inline citations.
      </p>
      <ChatUI />
      <p className="mt-10 text-xs text-stone-500">
        Requires <code>ANTHROPIC_API_KEY</code> in <code>app/.env.local</code>.
      </p>
    </div>
  );
}
