from groq import Groq

from app.core.config import settings
from app.llm.base import BaseLLM

class GroqLLM(BaseLLM):
    def __init__(self) -> None:
        self.client = Groq(
            api_key=settings.groq_api_key
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
        )