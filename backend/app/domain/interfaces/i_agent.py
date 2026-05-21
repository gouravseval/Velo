from abc import ABC, abstractmethod
from typing import AsyncIterator, TYPE_CHECKING
from app.domain.entities.agent import AgentMetadata
from app.domain.entities.run import Run, RunRecord

if TYPE_CHECKING:
    from app.domain.entities.task import Task


class BaseAgent(ABC):
    """
    Every agent must implement this interface.
    The framework calls execute() and streams RunRecord events.
    """

    @classmethod
    @abstractmethod
    def metadata(cls) -> AgentMetadata:
        """Static description of this agent. Called at registration time."""
        ...

    @abstractmethod
    async def validate_task(self, task: "Task") -> list[str]:
        """
        Validate the task before execution.
        Return list of error strings (empty = valid).
        """
        ...

    @abstractmethod
    async def execute(
        self,
        task: "Task",
        run: Run,
    ) -> AsyncIterator[RunRecord]:
        """
        Core execution loop. Yields one RunRecord per processed item.
        The orchestrator collects these and publishes SSE events.
        """
        ...
