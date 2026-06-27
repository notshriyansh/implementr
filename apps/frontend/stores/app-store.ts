import { create } from "zustand";

import { AppState, AppActions } from "@/types/app-state";

export const useAppStore = create<AppState & AppActions>((set) => ({
  selectedPaper: undefined,
  selectedRepository: undefined,
  selectedFile: undefined,
  selectedChunk: undefined,
  recentPapers: [],
  recentRepositories: [],
  recentQuestions: [],
  workspaceQuestion: undefined,
  commandOpen: false,

  setSelectedPaper: (paper) =>
    set({
      selectedPaper: paper,
    }),

  setSelectedRepository: (repo) =>
    set({
      selectedRepository: repo,
    }),

  setSelectedFile: (file) =>
    set({
      selectedFile: file,
    }),

  setSelectedChunk: (chunk) =>
    set({
      selectedChunk: chunk,
    }),

  addRecentPaper: (paper) =>
    set((state) => ({
      recentPapers: [paper, ...state.recentPapers].slice(0, 5),
    })),

  addRecentRepository: (repo) =>
    set((state) => ({
      recentRepositories: [repo, ...state.recentRepositories].slice(0, 5),
    })),

  addRecentQuestion: (question) =>
    set((state) => ({
      recentQuestions: [question, ...state.recentQuestions].slice(0, 10),
    })),

  setWorkspaceQuestion: (question) =>
    set({
      workspaceQuestion: question,
    }),

  setCommandOpen: (open) =>
    set({
      commandOpen: open,
    }),

  clearWorkspace: () =>
    set({
      selectedFile: undefined,
      selectedChunk: undefined,
      workspaceQuestion: undefined,
    }),
}));
