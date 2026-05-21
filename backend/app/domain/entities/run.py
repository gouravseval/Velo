from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
from typing import Optional, Any


class RunStatus(str, Enum):
    PENDING = "pending"
    EXTRACTING = "extracting"
    CALLING_API = "calling_api"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


@dataclass
class RunRecord:
    """Result of a single record processed by an agent."""
    index: int
    raw_data: dict[str, Any]
    extracted_data: Optional[dict[str, Any]] = None
    api_response: Optional[dict[str, Any]] = None
    status: str = "pending"          # pending | success | failed | skipped
    error: Optional[str] = None
    http_status_code: Optional[int] = None
    retries: int = 0


@dataclass
class Run:
    id: str
    task_id: str
    agent_id: str
    status: RunStatus = RunStatus.PENDING
    total_records: int = 0
    processed_records: int = 0
    success_count: int = 0
    failed_count: int = 0
    skipped_count: int = 0
    records: list[RunRecord] = field(default_factory=list)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    error_message: Optional[str] = None
    dry_run: bool = False
