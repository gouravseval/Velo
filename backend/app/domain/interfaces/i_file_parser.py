from abc import ABC, abstractmethod
from typing import Any


class IFileParser(ABC):
    @abstractmethod
    def parse(self, data: bytes) -> list[dict[str, Any]]:
        """Parse raw bytes into a list of row dicts."""
        ...
