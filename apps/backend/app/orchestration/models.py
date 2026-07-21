from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class JobExecutionResult:

    result: dict[str, Any]