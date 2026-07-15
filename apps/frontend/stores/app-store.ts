import { create } from "zustand";
import { persist } from "zustand/middleware";

import { AppState, AppActions } from "@/types/app-state";

export const useAppStore = create<AppState & AppActions>()(
  persist(
    (set) => ({
      selectedPaper: undefined,
      selectedRepository: undefined,
      selectedFile: undefined,
      selectedChunk: undefined,
      recentPapers: [],
      recentRepositories: [],
      recentQuestions: [],
      workspaceQuestion: undefined,
      commandOpen: false,
      blueprintTargetFile: undefined,
      blueprintTargetSymbol: undefined,
      blueprintTargetReason: undefined,

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

      setBlueprintTargetFile: (file) =>
        set({
          blueprintTargetFile: file,
        }),

      setBlueprintTargetSymbol: (symbol) =>
        set({
          blueprintTargetSymbol: symbol,
        }),

      setBlueprintTargetReason: (reason) =>
        set({
          blueprintTargetReason: reason,
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
    }),
    {
      name: "implementr-workspace-storage",
      version: 1,
      partialize: (state) => ({
        selectedPaper: state.selectedPaper,
        selectedRepository: state.selectedRepository,
        recentPapers: state.recentPapers,
        recentRepositories: state.recentRepositories,
        recentQuestions: state.recentQuestions,
        workspaceQuestion: state.workspaceQuestion,
        blueprintTargetFile: state.blueprintTargetFile,
        blueprintTargetSymbol: state.blueprintTargetSymbol,
        blueprintTargetReason: state.blueprintTargetReason,
      }),
    },
  ),
);
