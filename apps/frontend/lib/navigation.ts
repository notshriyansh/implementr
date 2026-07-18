import {
  BookOpen,
  FolderGit2,
  Workflow,
  Network,
  ClipboardList,
} from "lucide-react";

export const navigationItems = [
  {
    label: "Research",
    href: "/research",
    icon: BookOpen,
    number: "01",
  },
  {
    label: "Repository",
    href: "/repository",
    icon: FolderGit2,
    number: "02",
  },
  {
    label: "Architecture",
    href: "/architecture",
    icon: Network,
    number: "03",
  },
  {
    label: "Workspace",
    href: "/workspace",
    icon: Workflow,
    number: "04",
  },
  {
    label: "History",
    href: "/workspaces",
    icon: ClipboardList,
    number: "05",
  },
];
