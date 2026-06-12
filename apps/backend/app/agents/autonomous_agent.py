from app.llm.base import BaseLLM
from app.tools.planning_tool import (
    PlanningTool,
)
from app.tools.retrieval_tool import (
    RetrievalTool,
)


class AutonomousResearchAgent:
    def __init__(
        self,
        llm: BaseLLM,
        retrieval_tool: RetrievalTool,
        planning_tool: PlanningTool,
    ) -> None:
        self.llm = llm

        self.retrieval_tool = (
            retrieval_tool
        )

        self.planning_tool = (
            planning_tool
        )

    async def decide_actions(
        self,
        question: str,
    ) -> str:
        prompt = f"""
    You are an autonomous research agent.

    Decide what actions are needed.

    Available tools:
    - retrieval
    - planning

    Question:
    {question}

    Respond with:
    RETRIEVE_AND_PLAN
    or
    PLAN_ONLY
    """

        return await self.llm.generate(
            prompt
        )
    
    async def run(
        self,
        question: str,
    ) -> str:
        decision = (
            await self.decide_actions(
                question
            )
        )

        if "RETRIEVE" in decision:
            context = (
                await self.retrieval_tool.run(
                    question
                )
            )

            plan = (
                await self.planning_tool.run(
                    context=context,
                    goal=question,
                )
            )

            return plan

        return await self.planning_tool.run(
            context="",
            goal=question,
        )