import { ChatMessage as Message } from "@/types/chat";

interface Props {
  message: Message;
}

export function ChatMessage({ message }: Props) {
  const isUser = message.role === "user";

  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-3xl rounded-2xl px-4 py-3 ${
          isUser ? "bg-primary text-primary-foreground" : "bg-muted"
        }`}
      >
        <div className="whitespace-pre-wrap text-sm">{message.content}</div>

        {message.citations && message.citations.length > 0 && (
          <div className="mt-4 flex gap-2 flex-wrap">
            {message.citations.map((citation, index) => (
              <div key={index} className="text-xs rounded-lg border px-2 py-1">
                p.
                {citation.page_number}
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}
