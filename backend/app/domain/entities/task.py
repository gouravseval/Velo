from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class Task:
    """Represents a single run request from the user."""
    id: str
    agent_id: str
    file_bytes: bytes
    file_name: str
    file_content_type: str
    curl_command: str
    dry_run: bool = False
    concurrency: int = 3
    config: dict[str, Any] = field(default_factory=dict)
