import { Badge } from "@/components/ui/badge";

const featuredPapers = [
  {
    title: "FlashAttention-2: Faster Attention with Better Parallelism",
    author: "Tri Dao",
    year: "2023",
    status: "INGESTED",
    tags: ["attention", "cuda", "kernels"],
  },
  {
    title: "Mistral 7B",
    author: "Jiang et al.",
    year: "2023",
    status: "INDEXED",
    tags: ["llm", "gqa"],
  },
  {
    title: "Attention Is All You Need",
    author: "Vaswani et al.",
    year: "2017",
    status: "INGESTED",
    tags: ["transformers"],
  },
];

export function RecentPapersTable() {
  return (
    <div className="rounded-xl border overflow-hidden">
      <div className="grid grid-cols-12 px-6 py-4 border-b text-xs uppercase tracking-wider text-muted-foreground">
        <div className="col-span-7">Title</div>
        <div className="col-span-3">Tags</div>
        <div className="col-span-2">Status</div>
      </div>

      {featuredPapers.map((paper) => (
        <div
          key={paper.title}
          className="grid grid-cols-12 px-6 py-5 border-b items-center"
        >
          <div className="col-span-7">
            <div className="font-medium">{paper.title}</div>

            <div className="text-sm text-muted-foreground mt-1">
              {paper.author} · {paper.year}
            </div>
          </div>

          <div className="col-span-3 flex gap-2 flex-wrap">
            {paper.tags.map((tag) => (
              <Badge key={tag} variant="outline">
                {tag}
              </Badge>
            ))}
          </div>

          <div className="col-span-2">
            <Badge>{paper.status}</Badge>
          </div>
        </div>
      ))}
    </div>
  );
}
