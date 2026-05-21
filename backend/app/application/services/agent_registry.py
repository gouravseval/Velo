import importlib
import pkgutil
import inspect
from typing import Type
from app.domain.interfaces.i_agent import BaseAgent
from app.domain.entities.agent import AgentMetadata


class AgentRegistry:
    """
    Discovers and holds all registered agents.
    Agents are auto-discovered from the `agents/` package.

    OPEN/CLOSED: adding an agent never modifies this class.
    """

    def __init__(self):
        self._agents: dict[str, Type[BaseAgent]] = {}

    def discover(self, agents_package: str = "app.agents") -> None:
        """
        Walk the agents package and register any class that
        subclasses BaseAgent (excluding BaseAgent itself).
        """
        package = importlib.import_module(agents_package)
        for _, module_name, is_pkg in pkgutil.walk_packages(
            path=package.__path__,
            prefix=package.__name__ + ".",
            onerror=lambda x: None,
        ):
            module = importlib.import_module(module_name)
            for _, obj in inspect.getmembers(module, inspect.isclass):
                if (
                    issubclass(obj, BaseAgent)
                    and obj is not BaseAgent
                    and not inspect.isabstract(obj)
                ):
                    meta = obj.metadata()
                    self._agents[meta.id] = obj

    def get(self, agent_id: str) -> Type[BaseAgent]:
        if agent_id not in self._agents:
            raise KeyError(f"Agent '{agent_id}' not found in registry")
        return self._agents[agent_id]

    def list_all(self) -> list[AgentMetadata]:
        return [cls.metadata() for cls in self._agents.values()]

    def instantiate(self, agent_id: str, **deps) -> BaseAgent:
        """Create an agent instance with injected dependencies."""
        cls = self.get(agent_id)
        return cls(**deps)
