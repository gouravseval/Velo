from app.application.services.agent_registry import AgentRegistry
from app.domain.entities.agent import AgentMetadata


class ListAgentsUseCase:
    def __init__(self, registry: AgentRegistry):
        self._registry = registry

    def execute(self) -> list[AgentMetadata]:
        return self._registry.list_all()
