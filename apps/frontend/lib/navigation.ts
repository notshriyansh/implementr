import {
  BookOpen,
  FolderGit2,
  Workflow,
  Network,
  ClipboardList,
  Hammer,
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
    label: "Reproduction",
    href: "/reproduction",
    icon: ClipboardList,
    number: "05",
  },
  {
    label: "Blueprints",
    href: "/blueprints",
    icon: Hammer,
    number: "06",
  },
  {
    label: "Evaluation",
    href: "/evaluation",
    icon: BarChart3,
    number: "07",
  },
];
