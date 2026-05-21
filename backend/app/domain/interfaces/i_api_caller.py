from abc import ABC, abstractmethod
from typing import Any
from app.domain.entities.api_spec import ApiSpec
from app.domain.value_objects.api_call_result import ApiCallResult


class IApiCaller(ABC):
    @abstractmethod
    async def call(
        self,
        spec: ApiSpec,
        record_data: dict[str, Any],
        dry_run: bool = False,
    ) -> ApiCallResult:
        ...
