from dataclasses import dataclass, field
from typing import Any


@dataclass
class ExtractionResult:
    index: int
    data: dict[str, Any]
    confidence: float = 1.0
    warnings: list[str] = field(default_factory=list)
