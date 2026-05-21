import asyncio
import httpx
from typing import Any, Optional, Tuple
from app.domain.entities.api_spec import ApiSpec, HttpMethod
from app.domain.value_objects.api_call_result import ApiCallResult


class ApiCaller:
    """
    Executes API calls for a single record.
    Supports retry with exponential backoff.
    Fills {placeholder} tokens in URL and body from record data.
    """

    def __init__(
        self,
        max_retries: int = 3,
        retry_on_status: tuple[int, ...] = (429, 500, 502, 503, 504),
    ):
        self._max_retries = max_retries
        self._retry_on_status = retry_on_status

    async def call(
        self,
        spec: ApiSpec,
        record_data: dict[str, Any],
        dry_run: bool = False,
    ) -> ApiCallResult:
        url = self._fill_template(spec.url, record_data)
        body = self._fill_body(spec.body_template, record_data)
        headers = dict(spec.headers)

        if dry_run:
            return ApiCallResult(
                success=True,
                status_code=0,
                response_body={"dry_run": True, "would_call": url, "body": body},
            )

        attempt = 0
        last_error = None

        async with httpx.AsyncClient(timeout=spec.timeout_seconds) as client:
            while attempt <= self._max_retries:
                try:
                    resp = await client.request(
                        method=spec.method.value,
                        url=url,
                        headers=headers,
                        json=body if body else None,
                    )
                    if resp.status_code in self._retry_on_status and attempt < self._max_retries:
                        wait = 2 ** attempt
                        await asyncio.sleep(wait)
                        attempt += 1
                        continue

                    try:
                        resp_body = resp.json()
                    except Exception:
                        resp_body = {"raw": resp.text}

                    return ApiCallResult(
                        success=resp.is_success,
                        status_code=resp.status_code,
                        response_body=resp_body,
                        retries=attempt,
                    )
                except httpx.RequestError as e:
                    last_error = str(e)
                    await asyncio.sleep(2 ** attempt)
                    attempt += 1

        return ApiCallResult(
            success=False,
            status_code=0,
            error=last_error or "Max retries exceeded",
            retries=attempt,
        )

    def _fill_template(self, template: str, data: dict) -> str:
        """Replace {key} placeholders in URL."""
        for key, value in data.items():
            template = template.replace(f"{{{key}}}", str(value))
        return template

    def _fill_body(
        self,
        template: Optional[dict],
        data: dict,
    ) -> Optional[dict]:
        if not template:
            return None
        filled = {}
        for k, v in template.items():
            if isinstance(v, str) and v.startswith("{") and v.endswith("}"):
                field_name = v[1:-1]
                filled[k] = data.get(field_name, v)
            else:
                filled[k] = v
        return filled
