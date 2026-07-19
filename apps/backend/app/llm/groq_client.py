from collections.abc import AsyncGenerator

from groq import Groq

from app.core.config import settings
from app.llm.base import BaseLLM

from app.observability.tracing import (
    trace_execution,
)


class GroqLLM(BaseLLM):
    def __init__(self) -> None:
        self.client = Groq(
            api_key=settings.groq_api_key,
        )

    @trace_execution(
    "groq.generate"
)

    async def generate(
        self,
        prompt: str,
    ) -> str:
        response = (
            self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0.2,
            )
        )

        return (
            response.choices[0]
            .message.content
            or ""
        )
    
    @trace_execution(
    "groq.stream_generate"
)

    async def stream_generate(
        self,
        prompt: str,
    ) -> AsyncGenerator[str, None]:
        stream = (
            self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {
                        "role": "user",
                        "content": prompt,
                    }
                ],
                temperature=0.2,
                stream=True,
            )
        )

        for chunk in stream:
            content = (
                chunk.choices[0]
                .delta.content
            )

            if content:
                yield content