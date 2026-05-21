from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.run import Run


class IRunRepository(ABC):
    @abstractmethod
    async def save(self, run: Run) -> None:
        ...

    @abstractmethod
    async def get(self, run_id: str) -> Optional[Run]:
        ...

    @abstractmethod
    async def list_all(self) -> list[Run]:
        ...
