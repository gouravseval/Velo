from abc import ABC, abstractmethod
from typing import Any
from app.domain.value_objects.extraction_result import ExtractionResult


class IExtractor(ABC):
    @abstractmethod
    async def extract_batch(
        self,
        rows: list[dict[str, Any]],
        schema: dict[str, Any],
        instructions: str = "",
    ) -> list[ExtractionResult]:
        ...
