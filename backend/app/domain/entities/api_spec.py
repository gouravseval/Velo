from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Any


class HttpMethod(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    PATCH = "PATCH"
    DELETE = "DELETE"


@dataclass
class ApiSpec:
    """
    Parsed representation of a curl command.
    Body may contain {placeholders} that get filled per record.
    e.g. {"rating": "{rating}", "review": "{review_text}"}
    """
    method: HttpMethod
    url: str
    headers: dict[str, str] = field(default_factory=dict)
    body_template: Optional[dict[str, Any]] = None
    query_params: dict[str, str] = field(default_factory=dict)
    timeout_seconds: float = 30.0
