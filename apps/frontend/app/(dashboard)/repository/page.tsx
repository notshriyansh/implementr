"use client";

import { useState } from "react";

import { CodeChunk, FileNode } from "@/types/repository";

import { RepositoryHeader } from "@/components/repository/repository-header";
import { RepositoryIngestForm } from "@/components/repository/repository-ingest-form";
import { RepositoryTree } from "@/components/repository/repository-tree";
import { RepositoryCodeViewer } from "@/components/repository/repository-code-viewer";
import { RepositorySearch } from "@/components/repository/repository-search";
import { RepositorySearchResults } from "@/components/repository/repository-search-results";
import { CodeChunkViewer } from "@/components/repository/code-chunk-viewer";
import { PageContainer } from "@/components/shared/page-container";

import { useRepositoryIngestion } from "@/hooks/use-repository-ingestion";
import { useRepositoryStructure } from "@/hooks/use-repository-structure";
import { useRepositorySearch } from "@/hooks/use-repository-search";
import { useAppStore } from "@/stores/app-store";

export default function RepositoryPage() {
  const [repoPath, setRepoPath] = useState("");
  const [selectedFile, setSelectedFile] = useState<FileNode>();
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedChunk, setSelectedChunk] = useState<CodeChunk>();

  const ingestMutation = useRepositoryIngestion();

  const structureQuery = useRepositoryStructure(repoPath, !!repoPath);

  const searchQueryResult = useRepositorySearch(searchQuery);

  const setSelectedRepository = useAppStore(
    (state) => state.setSelectedRepository,
  );

  const addRecentRepository = useAppStore((state) => state.addRecentRepository);

  const setSelectedFileStore = useAppStore((state) => state.setSelectedFile);

  async function handleAnalyze(path: string) {
    setRepoPath(path);

    setSelectedRepository(path);

    addRecentRepository(path);

    await ingestMutation.mutateAsync(path);
  }

  return (
    <PageContainer>
      <RepositoryHeader />

      <RepositoryIngestForm
        onAnalyze={handleAnalyze}
        loading={ingestMutation.isPending}
      />

      <div className="mt-8">
        <RepositorySearch onSearch={setSearchQuery} />
      </div>

      {structureQuery.data && (
        <div className="mt-8 grid grid-cols-1 gap-6 xl:grid-cols-12">
          <div className="xl:col-span-5">
            <RepositoryTree
              files={structureQuery.data.files}
              onSelect={(file) => {
                setSelectedFile(file);

                setSelectedFileStore(file);
              }}
            />
          </div>

          <div className="xl:col-span-7">
            <RepositoryCodeViewer file={selectedFile} />
          </div>
        </div>
      )}

      {searchQueryResult.data && (
        <div className="mt-8 grid grid-cols-1 gap-6 xl:grid-cols-12">
          <div className="xl:col-span-5">
            <RepositorySearchResults
              results={searchQueryResult.data.results}
              onSelect={setSelectedChunk}
            />
          </div>

          <div className="xl:col-span-7">
            <CodeChunkViewer chunk={selectedChunk} />
          </div>
        </div>
      )}
    </PageContainer>
  );
}
