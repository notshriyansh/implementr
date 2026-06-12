from pydantic import BaseModel


class ImplementationPlan(
    BaseModel,
):
    summary: str

    architecture: list[str]

    implementation_steps: list[str]

    challenges: list[str]

    suggested_stack: list[str]