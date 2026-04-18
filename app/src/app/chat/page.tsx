import ChatUI from "./ChatUI";

export default function ChatPage() {
  return (
    <div className="max-w-3xl">
      <h1 className="text-3xl font-bold tracking-tight">Chat with the vault</h1>
      <p className="mt-2 text-stone-600 text-sm">
        Ask questions grounded in the shipped lessons. Retrieves the most
        relevant excerpts from the vault, then answers through your local
        <code className="mx-1">claude</code> CLI with inline citations.
      </p>
      <ChatUI />
      <p className="mt-10 text-xs text-stone-500">
        Runs on your Claude Max subscription via the <code>claude</code> CLI —
        no API key required. Make sure <code>claude</code> is on PATH.
      </p>
    </div>
  );
}
