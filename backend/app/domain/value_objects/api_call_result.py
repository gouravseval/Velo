from dataclasses import dataclass, field
from typing import Optional, Any


@dataclass
class ApiCallResult:
    success: bool
    status_code: int
    response_body: Optional[dict[str, Any]] = None
    error: Optional[str] = None
    retries: int = 0
