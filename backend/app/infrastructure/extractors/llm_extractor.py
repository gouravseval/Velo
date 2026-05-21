import json
from typing import Any
from app.domain.interfaces.i_extractor import IExtractor
from app.domain.value_objects.extraction_result import ExtractionResult

try:
    from anthropic import AsyncAnthropic
    HAS_ANTHROPIC = True
except ImportError:
    HAS_ANTHROPIC = False


class LLMExtractor(IExtractor):
    """
    Given raw rows from a file and a target JSON schema,
    asks the LLM to extract structured data.

    Sends rows in batches for efficiency.
    """

    def __init__(self, client: "AsyncAnthropic", model: str = "claude-sonnet-4-20250514"):
        self._client = client
        self._model = model

    async def extract_batch(
        self,
        rows: list[dict[str, Any]],
        schema: dict[str, Any],
        instructions: str = "",
    ) -> list[ExtractionResult]:
        prompt = self._build_prompt(rows, schema, instructions)

        response = await self._client.messages.create(
            model=self._model,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )

        raw = response.content[0].text
        # Strip markdown fences if present
        raw = raw.strip().removeprefix("```json").removesuffix("```").strip()

        parsed: list[dict] = json.loads(raw)
        return [
            ExtractionResult(
                index=i,
                data=item.get("data", {}),
                confidence=item.get("confidence", 1.0),
                warnings=item.get("warnings", []),
            )
            for i, item in enumerate(parsed)
        ]

    def _build_prompt(
        self,
        rows: list[dict],
        schema: dict,
        instructions: str,
    ) -> str:
        return f"""You are a data extraction assistant.

Extract structured data from each row according to the schema below.
Return ONLY a JSON array — no markdown, no explanation.

## Target Schema
{json.dumps(schema, indent=2)}

## Additional Instructions
{instructions or "None"}

## Input Rows
{json.dumps(rows, indent=2)}

## Response Format
Return a JSON array of objects, one per input row:
[
  {{
    "data": {{ /* extracted fields matching schema */ }},
    "confidence": 0.0-1.0,
    "warnings": ["optional notes about missing/ambiguous fields"]
  }}
]"""
