from app.llm.base import BaseLLM


class PlanningTool:
    def __init__(
        self,
        llm: BaseLLM,
    ) -> None:
        self.llm = llm

    async def run(
        self,
        context: str,
        goal: str,
    ) -> str:
        prompt = f"""
Create an implementation plan.

Goal:
{goal}

Context:
{context}
"""

        return await self.llm.generate(
            prompt
        )