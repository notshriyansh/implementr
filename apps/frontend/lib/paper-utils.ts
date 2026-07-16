import { Paper } from "@/types/paper";

export function uniquePapers(papers: Paper[]) {
  const map = new Map<string, Paper>();

  for (const paper of papers) {
    map.set(paper.pdf_url, paper);
  }

  return [...map.values()];
}
