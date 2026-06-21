"use client";

import { useState } from "react";

import { FileNode } from "@/types/repository";

import { RepositoryHeader } from "@/components/repository/repository-header";
import { RepositoryIngestForm } from "@/components/repository/repository-ingest-form";
import { RepositoryFileList } from "@/components/repository/repository-file-list";
import { RepositoryCodeViewer } from "@/components/repository/repository-code-viewer";

import { useRepositoryIngestion } from "@/hooks/use-repository-ingestion";
import { useRepositoryStructure } from "@/hooks/use-repository-structure";

export default function RepositoryPage() {
  const [repoPath, setRepoPath] = useState("");

  const [selectedFile, setSelectedFile] = useState<FileNode>();

  const ingestMutation = useRepositoryIngestion();

  const structureQuery = useRepositoryStructure(repoPath, !!repoPath);

  async function handleAnalyze(path: string) {
    setRepoPath(path);

    await ingestMutation.mutateAsync(path);
  }

  return (
    <div className="max-w-7xl mx-auto p-8">
      <RepositoryHeader />

      <RepositoryIngestForm
        onAnalyze={handleAnalyze}
        loading={ingestMutation.isPending}
      />

      {structureQuery.data && (
        <div className="grid grid-cols-12 gap-6 mt-8">
          <div className="col-span-4">
            <RepositoryFileList
              files={structureQuery.data.files}
              onSelect={setSelectedFile}
            />
          </div>

          <div className="col-span-8">
            <RepositoryCodeViewer file={selectedFile} />
          </div>
        </div>
      )}
    </div>
  );
}
