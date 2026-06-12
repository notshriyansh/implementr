from langgraph.graph import (
    END,
    StateGraph,
)

from app.agents.state import (
    ResearchState,
)
from app.llm.base import BaseLLM
from app.retrieval.retrieval_service import (
    RetrievalService,
)

class ResearchGraph:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        llm: BaseLLM,
    ) -> None:
        self.retrieval_service = (
            retrieval_service
        )

        self.llm = llm

        self.graph = (
            self._build_graph()
        )


    async def retrieve_context(
        self,
        state: ResearchState,
    ) -> ResearchState:
        chunks = (
            await self.retrieval_service.retrieve(
                query=state["question"],
                k=6,
            )
        )

        context = "\n\n".join(
            chunk.text
            for chunk in chunks
        )

        state["retrieved_context"] = (
            context
        )

        return state
    

    async def analyze_methodology(
        self,
        state: ResearchState,
    ) -> ResearchState:
        prompt = f"""
    Analyze the methodology described
    in this research context.

    Focus on:
    - architecture
    - learning strategy
    - training setup
    - major innovations

    Context:
    {state["retrieved_context"]}
    """

        response = await self.llm.generate(
            prompt
        )

        state["methodology_analysis"] = (
            response
        )

        return state
    

    async def generate_plan(
        self,
        state: ResearchState,
    ) -> ResearchState:
        prompt = f"""
    Create a practical implementation
    plan for this research paper.

    Methodology:
    {state["methodology_analysis"]}

    Context:
    {state["retrieved_context"]}
    """

        response = await self.llm.generate(
            prompt
        )

        state["implementation_plan"] = (
            response
        )

        return state
    

    async def analyze_challenges(
        self,
        state: ResearchState,
    ) -> ResearchState:
        prompt = f"""
    Identify the engineering challenges
    in implementing this system.

    Implementation Plan:
    {state["implementation_plan"]}
    """

        response = await self.llm.generate(
            prompt
        )

        state["challenges"] = response

        return state
    

    async def finalize(
        self,
        state: ResearchState,
    ) -> ResearchState:
        state["final_answer"] = f"""
    # Methodology Analysis

    {state["methodology_analysis"]}

    # Implementation Plan

    {state["implementation_plan"]}

    # Engineering Challenges

    {state["challenges"]}
    """

        return state
    
    def _build_graph(
        self,
    ):
        workflow = StateGraph(
            ResearchState
        )

        workflow.add_node(
            "retrieve",
            self.retrieve_context,
        )

        workflow.add_node(
            "methodology",
            self.analyze_methodology,
        )

        workflow.add_node(
            "implementation",
            self.generate_plan,
        )

        workflow.add_node(
            "challenges",
            self.analyze_challenges,
        )

        workflow.add_node(
            "finalize",
            self.finalize,
        )

        workflow.set_entry_point(
            "retrieve"
        )

        workflow.add_edge(
            "retrieve",
            "methodology",
        )

        workflow.add_edge(
            "methodology",
            "implementation",
        )

        workflow.add_edge(
            "implementation",
            "challenges",
        )

        workflow.add_edge(
            "challenges",
            "finalize",
        )

        workflow.add_edge(
            "finalize",
            END,
        )

        return workflow.compile()
    
    async def run(
        self,
        question: str,
    ) -> str:
        result = await self.graph.ainvoke(
            {
                "question": question,
                "retrieved_context": "",
                "methodology_analysis": "",
                "implementation_plan": "",
                "challenges": "",
                "final_answer": "",
            }
        )

        return result["final_answer"]