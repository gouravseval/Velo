from typing import Optional
from app.application.services.agent_registry import AgentRegistry
from app.domain.interfaces.i_run_repository import IRunRepository
from app.domain.entities.run import Run


class GetRunStatusUseCase:
    def __init__(self, run_repo: IRunRepository):
        self._run_repo = run_repo

    async def execute(self, run_id: str) -> Optional[Run]:
        return await self._run_repo.get(run_id)
