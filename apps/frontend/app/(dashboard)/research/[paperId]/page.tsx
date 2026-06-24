import { PaperWorkspace } from "@/components/workspace/paper-workspace";
import { PaperHeader } from "@/components/workspace/paper-header";

export default async function PaperWorkspacePage({
  params,
}: {
  params: Promise<{
    paperId: string;
  }>;
}) {
  const { paperId } = await params;

  return (
    <div className="max-w-350] mx-auto p-8">
      <PaperHeader paperId={paperId} />

      <PaperWorkspace />
    </div>
  );
}
