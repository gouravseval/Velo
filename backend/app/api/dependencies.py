"""
Dependency injection container.
All singletons are created here and injected via FastAPI Depends.
"""
from functools import lru_cache
from typing import Optional
from app.application.services.agent_registry import AgentRegistry
from app.application.use_cases.execute_run import ExecuteRunUseCase
from app.application.use_cases.list_agents import ListAgentsUseCase
from app.application.use_cases.get_run_status import GetRunStatusUseCase
from app.infrastructure.persistence.in_memory_run_repo import InMemoryRunRepository
from app.infrastructure.streaming.sse_event_bus import SseEventBus
from app.infrastructure.extractors.llm_extractor import LLMExtractor
from app.infrastructure.http.api_caller import ApiCaller
from app.infrastructure.http.curl_parser import CurlParser
from app.infrastructure.parsers.parser_factory import ParserFactory
from app.config import settings

# ── Singletons ──────────────────────────────────────────────────────────────

_registry = AgentRegistry()
_run_repo = InMemoryRunRepository()
_event_bus = SseEventBus()
_parser_factory = ParserFactory()
_curl_parser = CurlParser()
_api_caller = ApiCaller(max_retries=settings.max_retries)

# Anthropic client — only created if API key is set
_extractor: Optional[LLMExtractor] = None

if settings.anthropic_api_key:
    try:
        from anthropic import AsyncAnthropic
        _extractor = LLMExtractor(
            client=AsyncAnthropic(api_key=settings.anthropic_api_key),
            model=settings.llm_model,
        )
    except ImportError:
        pass


def startup_registry() -> None:
    """Called at application startup to discover all agents."""
    _registry.discover()


# ── FastAPI dependency callables ─────────────────────────────────────────────

def get_agent_registry() -> AgentRegistry:
    return _registry


def get_run_repo() -> InMemoryRunRepository:
    return _run_repo


def get_event_bus() -> SseEventBus:
    return _event_bus


def get_execute_run_use_case() -> ExecuteRunUseCase:
    return ExecuteRunUseCase(
        registry=_registry,
        run_repo=_run_repo,
        event_bus=_event_bus,
        extractor=_extractor,
        api_caller=_api_caller,
        parser_factory=_parser_factory,
        curl_parser=_curl_parser,
    )


def get_list_agents_use_case() -> ListAgentsUseCase:
    return ListAgentsUseCase(_registry)


def get_run_status_use_case() -> GetRunStatusUseCase:
    return GetRunStatusUseCase(_run_repo)
