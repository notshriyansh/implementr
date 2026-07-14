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
  summary: string;
  relevant_files: string[];
  relevant_symbols: string[];
  implementation_steps: string[];
  risks: string[];
  confidence: number;
  reasoning: string;
}

export interface FileContent {
  path: string;
  content: string;
  language: string;
  size_bytes: number;
  line_count: number;
}

export interface ResearchReproductionPlan {
  paper_summary: string;
  repository_targets: string[];
  required_changes: string[];
  training_changes: string[];
  evaluation_changes: string[];
  benchmark_tasks: string[];
  success_criteria: string[];
  risks: string[];
  confidence: number;
  concept_mappings: string[];
  architecture_gaps: string[];
  implementation_steps: string[];
  modification_targets: string[];
  gap_to_symbol_mapping: string[];
}

export interface BlueprintStep {
  file_path: string;
  symbol_name: string;
  change_type: string;
  reason: string;
  implementation_steps: string[];
  validation_steps: string[];
  expected_outcome: string;
}

export interface ImplementationBlueprint {
  paper_summary: string;
  blueprint_steps: BlueprintStep[];
  risks: string[];
  confidence: number;
}

export interface BlueprintEvaluationResult {
  target_file_score: number;
  target_symbol_score: number;
  gap_coverage_score: number;
  implementation_score: number;
  risk_score: number;
  overall_score: number;
}
