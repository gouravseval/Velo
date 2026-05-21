from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AgentMetadata:
    """Describes what an agent does and what input it expects."""
    id: str
    name: str
    description: str
    version: str
    input_file_types: list[str]
    extraction_schema: dict[str, Any]
    required_api_fields: list[str]
    supports_dry_run: bool = True
    max_concurrency: int = 5
