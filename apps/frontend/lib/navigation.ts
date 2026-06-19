import {
  BookOpen,
  FolderGit2,
  Workflow,
  Network,
  BarChart3,
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
    label: "Workspace",
    href: "/workspace",
    icon: Workflow,
    number: "03",
  },
  {
    label: "Architecture",
    href: "/architecture",
    icon: Network,
    number: "04",
  },
  {
    label: "Evaluation",
    href: "/evaluation",
    icon: BarChart3,
    number: "05",
  },
];
