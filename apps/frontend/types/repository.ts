export interface CodeChunk {
  chunk_id: string;
  file_path: string;
  language: string;
  content: string;
  start_line: number;
  end_line: number;
}

export interface RepositoryIngestResponse {
  total_chunks: number;
  sample_chunk: CodeChunk | null;
}

export interface FileNode {
  path: string;
  imports: string[];
  functions: string[];
  classes: string[];
}

export interface RepositoryMap {
  files: FileNode[];
}

export interface CodeSymbol {
  symbol_id: string;
  file_path: string;
  symbol_name: string;
  symbol_type: string;
  code: string;
  start_line: number;
  end_line: number;
}

export interface ArchitectureInsight {
  query: string;
  summary: string;
  relevant_files: string[];
  relevant_symbols: string[];
  execution_steps: string[];
  engineering_notes: string[];
  modification_points: string[];
  confidence: number;
  reasoning: string;
}

export interface HybridAnalysisResponse {
  result: string;
}
