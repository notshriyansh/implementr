"use client";

import { useMemo, useState } from "react";
import { toast } from "sonner";
import { motion } from "framer-motion";

import { Paper } from "@/types/paper";

import { PaperSearchBar } from "@/components/research/paper-search-bar";
import { PaperTable } from "@/components/research/paper-table";
import { ResearchHeader } from "@/components/research/research-header";
import { RecentPapersTable } from "@/components/research/recent-papers-table";

import { useDebounce } from "@/hooks/use-debounce";
import { usePaperSearch } from "@/hooks/use-paper-search";
import { usePaperIngestion } from "@/hooks/use-paper-ingestion";

function generatePaperId(title: string) {
  return title
    .toLowerCase()
    .replace(/[^a-z0-9]+/g, "-")
    .replace(/^-|-$/g, "");
}

export default function ResearchPage() {
  const [query, setQuery] = useState("");
  const [ingestingPaper, setIngestingPaper] = useState<string>();

  const debouncedQuery = useDebounce(query);

  const { data, isLoading, error } = usePaperSearch(debouncedQuery);

  const ingestionMutation = usePaperIngestion();

  const papers = useMemo(() => data?.papers ?? [], [data]);

  async function handleIngest(paper: Paper) {
    try {
      setIngestingPaper(paper.pdf_url);

      const paperId = generatePaperId(paper.title);

      const result = await ingestionMutation.mutateAsync({
        pdfUrl: paper.pdf_url,
        paperId,
      });

      toast.success(`${paper.title} ingested successfully`);

      console.log(result);
    } catch (error) {
      console.error(error);

      toast.error("Failed to ingest paper");
    } finally {
      setIngestingPaper(undefined);
    }
  }

  return (
    <motion.div
      initial={{ opacity: 0, y: 12 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.35 }}
      className="p-8 max-w-350] mx-auto"
    >
      <div className="mb-10">
        <ResearchHeader />
      </div>

      <div className="mb-8">
        <PaperSearchBar value={query} onChange={setQuery} />
      </div>

      {!query && <RecentPapersTable />}

      {isLoading && (
        <div className="text-muted-foreground">Searching papers...</div>
      )}

      {error && <div className="text-red-500">Failed to load papers.</div>}

      {!isLoading && papers.length > 0 && (
        <PaperTable
          papers={papers}
          onIngest={handleIngest}
          ingestingPaper={ingestingPaper}
        />
      )}

      {!isLoading && query && papers.length === 0 && (
        <div className="text-center py-24 text-muted-foreground">
          No papers found.
        </div>
      )}
    </motion.div>
  );
}
