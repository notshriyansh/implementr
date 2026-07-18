import { Paper } from "./paper";
import { FileNode, CodeChunk } from "./repository";

export interface AppState {
  selectedPaper?: Paper;
  selectedRepository?: string;
  selectedFile?: FileNode;
  selectedChunk?: CodeChunk;
  recentPapers: Paper[];
  recentRepositories: string[];
  recentQuestions: string[];
  workspaceQuestion?: string;
  commandOpen: boolean;
  blueprintTargetFile?: string;
  blueprintTargetSymbol?: string;
  blueprintTargetReason?: string;
  sessionStartedAt?: string;
  workspaceId?: string;
  workspaceName?: string;
}

export interface AppActions {
  setSelectedPaper: (paper: Paper) => void;
  setSelectedRepository: (repo: string) => void;
  setSelectedFile: (file: FileNode) => void;
  setSelectedChunk: (chunk: CodeChunk) => void;
  addRecentPaper: (paper: Paper) => void;
  addRecentRepository: (repo: string) => void;
  addRecentQuestion: (question: string) => void;
  setWorkspaceQuestion: (question: string) => void;
  setCommandOpen: (open: boolean) => void;
  clearWorkspace: () => void;
  setBlueprintTargetFile: (file: string) => void;
  setBlueprintTargetSymbol: (symbol: string) => void;
  setBlueprintTargetReason: (reason: string) => void;
  setSessionStartedAt: (date: string) => void;
  startNewSession: () => void;
  setWorkspaceId: (id: string) => void;
  setWorkspaceName: (name: string) => void;
  hydrateWorkspace: (payload: {
    workspaceId: string;
    workspaceName: string;
    selectedRepository?: string;
    workspaceQuestion?: string;
    blueprintTargetFile?: string;
    blueprintTargetSymbol?: string;
    blueprintTargetReason?: string;
  }) => void;
}
