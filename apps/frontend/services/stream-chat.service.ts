export async function streamPaperChat(
  sessionId: string,
  question: string,
  onChunk: (chunk: string) => void,
) {
  const response = await fetch(
    `${process.env.NEXT_PUBLIC_API_URL}/chat/stream?session_id=${sessionId}&question=${encodeURIComponent(question)}`,
    {
      method: "POST",
    },
  );

  if (!response.body) {
    throw new Error("No stream body");
  }

  const reader = response.body.getReader();

  const decoder = new TextDecoder();

  while (true) {
    const { done, value } = await reader.read();

    if (done) break;

    const chunk = decoder.decode(value);

    onChunk(chunk);
  }
}
