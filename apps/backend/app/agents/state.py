from typing import TypedDict


class ResearchState(TypedDict):
    question: str

    retrieved_context: str

    methodology_analysis: str

    implementation_plan: str

    challenges: str

    final_answer: str