export interface Workspace {
  id: string;
  name: string;

  selected_repository?: string;
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
  workspace_question?: string;

  blueprint_target_file?: string;
  blueprint_target_symbol?: string;
  blueprint_target_reason?: string;

  selected_paper?: string;
}

export interface WorkspaceOutput {
  id: string;
  workspace_id: string;

  hybrid_result?: unknown;
  reproduction_result?: unknown;
  blueprint_result?: unknown;
  evaluation_result?: unknown;
}
