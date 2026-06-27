"use client";

import { useMemo, useState } from "react";
import { toast } from "sonner";

import { LoadingSkeleton } from "@/components/shared/loading-skeleton";
import { EmptyState } from "@/components/shared/empty-state";
import { PageContainer } from "@/components/shared/page-container";

import { Paper } from "@/types/paper";

import { ResearchHeader } from "@/components/research/research-header";
import { PaperSearchBar } from "@/components/research/paper-search-bar";
import { PaperTable } from "@/components/research/paper-table";
import { RecentPapersTable } from "@/components/research/recent-papers-table";
import { useAppStore } from "@/stores/app-store";

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

  const setSelectedPaper = useAppStore((state) => state.setSelectedPaper);

  const addRecentPaper = useAppStore((state) => state.addRecentPaper);

  async function handleIngest(paper: Paper) {
    try {
      setIngestingPaper(paper.pdf_url);

      const paperId = generatePaperId(paper.title);

      await ingestionMutation.mutateAsync({
        pdfUrl: paper.pdf_url,
        paperId,
      });

      setSelectedPaper(paper);

      addRecentPaper(paper);

      toast.success(`${paper.title} ingested successfully`);
    } catch (error) {
      console.error(error);
      toast.error("Failed to ingest paper");
    } finally {
      setIngestingPaper(undefined);
    }
  }

  return (
    <PageContainer>
      <ResearchHeader />

      <div className="mt-10">
        <PaperSearchBar value={query} onChange={setQuery} />
      </div>

      {!query && (
        <div className="mt-10">
          <RecentPapersTable />
        </div>
      )}

      {isLoading && (
        <div className="mt-8">
          <LoadingSkeleton />
        </div>
      )}

      {error && (
        <div className="mt-10">
          <EmptyState
            title="Search failed"
            description="Something went wrong while searching arXiv."
          />
        </div>
      )}

      {!isLoading && papers.length > 0 && (
        <div className="mt-10">
          <PaperTable
            papers={papers}
            onIngest={handleIngest}
            ingestingPaper={ingestingPaper}
          />
        </div>
      )}

      {!isLoading && query && papers.length === 0 && (
        <div className="mt-10">
          <EmptyState
            title="No papers found"
            description="Try searching with different keywords, authors, or arXiv identifiers."
          />
        </div>
      )}
    </PageContainer>
  );
}
