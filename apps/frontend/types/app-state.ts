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
}
