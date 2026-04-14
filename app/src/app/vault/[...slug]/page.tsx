import { notFound } from "next/navigation";
import Link from "next/link";
import { readVaultFile, render } from "@/lib/vault";

export default async function VaultPage({
  params,
}: {
  params: Promise<{ slug: string[] }>;
}) {
  const { slug } = await params;
  const file = readVaultFile(slug);
  if (!file) return notFound();
  const rendered = await render(file);
  const title =
    (typeof file.data.title === "string" && file.data.title) ||
    slug[slug.length - 1];

  return (
    <div>
      <div className="text-sm text-stone-500">
        <Link href="/" className="hover:underline">home</Link> /{" "}
        {slug.slice(0, -1).map((part, i) => (
          <span key={i}>
            {part}
            {" / "}
          </span>
        ))}
        <span className="text-stone-700">{slug[slug.length - 1]}</span>
      </div>
      <h1 className="mt-3 text-3xl font-bold tracking-tight">{title}</h1>
      <div className="mt-1 text-xs text-stone-500">
        {rendered.readingMinutes} min read
      </div>
      <article
        className="prose-lesson mt-8"
        dangerouslySetInnerHTML={{ __html: rendered.html }}
      />
    </div>
  );
}
