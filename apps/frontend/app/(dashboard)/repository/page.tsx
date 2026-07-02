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
import { RepositoryDashboard } from "@/components/repository/repository-dashboard";
import { PanelLayout } from "@/components/layout/panel-layout";

import { useRepositoryIngestion } from "@/hooks/use-repository-ingestion";
import { useRepositoryStructure } from "@/hooks/use-repository-structure";
import { useRepositorySearch } from "@/hooks/use-repository-search";
import { useAppStore } from "@/stores/app-store";
import { useDebounce } from "@/hooks/use-debounce";

export default function RepositoryPage() {
  const [repoPath, setRepoPath] = useState("");
  const [selectedFile, setSelectedFile] = useState<FileNode>();
  const [searchQuery, setSearchQuery] = useState("");
  const [selectedChunk, setSelectedChunk] = useState<CodeChunk>();

  const ingestMutation = useRepositoryIngestion();
  const structureQuery = useRepositoryStructure(repoPath, !!repoPath);
  
  const debouncedSearchQuery = useDebounce(searchQuery, 300);
  const searchQueryResult = useRepositorySearch(debouncedSearchQuery);

  const setSelectedRepository = useAppStore(
    (state) => state.setSelectedRepository,
  );
  const addRecentRepository = useAppStore((state) => state.addRecentRepository);

  async function handleAnalyze(path: string) {
    setRepoPath(path);
    setSelectedRepository(path);
    addRecentRepository(path);
    await ingestMutation.mutateAsync(path);
  }

  const isSearching = searchQuery && searchQueryResult.data;

  return (
    <PanelLayout
      header={
        <div className="flex h-14 items-center justify-between px-6 bg-background">
          <RepositoryHeader />
          <div className="flex items-center gap-4">
            <RepositorySearch onSearch={setSearchQuery} />
            <RepositoryIngestForm
              onAnalyze={handleAnalyze}
              loading={ingestMutation.isPending}
            />
          </div>
        </div>
      }
      left={
        isSearching ? (
          <RepositorySearchResults
            results={searchQueryResult.data.results}
            onSelect={setSelectedChunk}
          />
        ) : structureQuery.data ? (
          <RepositoryTree
            files={structureQuery.data.files}
            onSelect={setSelectedFile}
            selectedFile={selectedFile?.path}
          />
        ) : null
      }
      center={
        isSearching ? (
          <CodeChunkViewer chunk={selectedChunk} />
        ) : structureQuery.data ? (
          <RepositoryCodeViewer file={selectedFile} />
        ) : (
          <div className="flex h-full items-center justify-center text-muted-foreground p-6 text-center">
            Analyze a repository to view its structure and file overview.
          </div>
        )
      }
      right={
        structureQuery.data && !isSearching ? (
          <RepositoryDashboard files={structureQuery.data.files} />
        ) : null
      }
    />
  );
}
