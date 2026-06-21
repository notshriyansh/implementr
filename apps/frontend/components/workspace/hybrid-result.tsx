import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

interface Props {
  result: string;
}

export function HybridResult({ result }: Props) {
  return (
    <div className="border rounded-xl p-8">
      <div className="mb-6">
        <h2 className="font-semibold text-xl">Implementation Guidance</h2>

        <p className="text-muted-foreground mt-2">
          Combined reasoning across paper context and repository context.
        </p>
      </div>

      <article className="prose prose-invert max-w-none">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{result}</ReactMarkdown>
      </article>
    </div>
  );
}
