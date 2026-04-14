import Link from "next/link";

export default function NotFound() {
  return (
    <div className="max-w-xl">
      <h1 className="text-3xl font-bold">Not found</h1>
      <p className="mt-3 text-stone-600">
        That page doesn't exist. Maybe the lesson hasn't been generated yet.
      </p>
      <div className="mt-6 space-x-4 text-sm">
        <Link href="/" className="text-accent hover:underline">Home</Link>
        <Link href="/search" className="text-accent hover:underline">Search</Link>
        <Link href="/vault/00-program/index" className="text-accent hover:underline">
          Program index
        </Link>
      </div>
    </div>
  );
}
