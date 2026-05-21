import copy
from typing import Optional
from app.domain.entities.run import Run
from app.domain.interfaces.i_run_repository import IRunRepository


class InMemoryRunRepository(IRunRepository):
    """Thread-safe in-memory run store. Suitable for development and testing."""

    def __init__(self):
        self._store: dict[str, Run] = {}

    async def save(self, run: Run) -> None:
        self._store[run.id] = copy.deepcopy(run)

    async def get(self, run_id: str) -> Optional[Run]:
        return copy.deepcopy(self._store.get(run_id))

    async def list_all(self) -> list[Run]:
        return [copy.deepcopy(r) for r in self._store.values()]

    async def delete(self, run_id: str) -> None:
        self._store.pop(run_id, None)
