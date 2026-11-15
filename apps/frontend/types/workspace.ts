import type {
  HybridAnalysisResponse,
  ResearchReproductionPlan,
  ImplementationBlueprint,
  BlueprintEvaluationResult,
} from "./repository";

export interface Workspace {
  id: string;
  name: string;

  selected_repository?: string;
  selected_repository_id?: string;
  workspace_question?: string;

  blueprint_target_file?: string;
  blueprint_target_symbol?: string;
  blueprint_target_reason?: string;

  selected_paper?: string;

  created_at?: string;
  updated_at?: string;
}

export interface CreateWorkspaceRequest {
  name: string;

  selected_repository?: string;
  selected_repository_id?: string;
  workspace_question?: string;

  blueprint_target_file?: string;
  blueprint_target_symbol?: string;
  blueprint_target_reason?: string;

  selected_paper?: string;
}

export interface WorkspaceOutput {
  id: string;
  workspace_id: string;
  hybrid_result?: HybridAnalysisResponse | null;
  reproduction_result?: ResearchReproductionPlan | null;
  blueprint_result?: ImplementationBlueprint | null;
  evaluation_result?: BlueprintEvaluationResult | null;
}
