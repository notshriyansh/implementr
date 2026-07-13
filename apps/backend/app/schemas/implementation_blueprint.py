from pydantic import BaseModel


class BlueprintStep(
    BaseModel,
):
    file_path: str

    symbol_name: str

    change_type: str

    reason: str

    implementation_steps: list[str]

    validation_steps: list[str]

    expected_outcome: str


class ImplementationBlueprint(
    BaseModel,
):
    paper_summary: str

    blueprint_steps: list[
        BlueprintStep
    ]

    risks: list[str]

    confidence: float