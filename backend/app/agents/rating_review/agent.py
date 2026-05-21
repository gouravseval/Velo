import asyncio
from typing import AsyncIterator
from app.domain.interfaces.i_agent import BaseAgent
from app.domain.entities.agent import AgentMetadata
from app.domain.entities.run import Run, RunRecord
from app.domain.entities.task import Task
from app.infrastructure.parsers.parser_factory import ParserFactory
from app.infrastructure.extractors.llm_extractor import LLMExtractor
from app.infrastructure.http.curl_parser import CurlParser
from app.infrastructure.http.api_caller import ApiCaller
from .schema import EXTRACTION_SCHEMA, EXTRACTION_INSTRUCTIONS

BATCH_SIZE = 10  # Extract 10 rows per LLM call


class RatingReviewAgent(BaseAgent):
    """
    Reads a file of ratings and reviews, extracts structured data via LLM,
    and calls the configured API endpoint for each record.
    """

    def __init__(
        self,
        extractor: LLMExtractor,
        api_caller: ApiCaller,
        parser_factory: ParserFactory,
        curl_parser: CurlParser,
    ):
        self._extractor = extractor
        self._api_caller = api_caller
        self._parser_factory = parser_factory
        self._curl_parser = curl_parser

    @classmethod
    def metadata(cls) -> AgentMetadata:
        return AgentMetadata(
            id="rating_review",
            name="API Executor with File Data",
            description=(
                "Upload a CSV, Excel, or JSON file. "
                "Each row is extracted into structured data using AI, "
                "then your API is called automatically for every record."
            ),
            version="1.0.0",
            input_file_types=["csv", "xlsx", "json"],
            extraction_schema=EXTRACTION_SCHEMA,
            required_api_fields=["product_id", "rating", "review_text"],
            supports_dry_run=True,
            max_concurrency=5,
        )

    async def validate_task(self, task: Task) -> list[str]:
        errors = []
        if not task.curl_command.strip():
            errors.append("curl_command is required")
        if not task.file_bytes:
            errors.append("A data file must be uploaded")
        try:
            self._curl_parser.parse(task.curl_command)
        except Exception as e:
            errors.append(f"Invalid curl command: {e}")
        return errors

    async def execute(self, task: Task, run: Run) -> AsyncIterator[RunRecord]:
        # Step 1: Parse the file into raw rows
        parser = self._parser_factory.get_parser(task.file_content_type, task.file_name)
        raw_rows = parser.parse(task.file_bytes)
        run.total_records = len(raw_rows)

        # Step 2: Parse the curl command
        api_spec = self._curl_parser.parse(task.curl_command)

        # Step 3: Extract in batches, then call API concurrently
        semaphore = asyncio.Semaphore(task.concurrency)

        for batch_start in range(0, len(raw_rows), BATCH_SIZE):
            batch = raw_rows[batch_start: batch_start + BATCH_SIZE]

            extraction_results = await self._extractor.extract_batch(
                rows=batch,
                schema=EXTRACTION_SCHEMA,
                instructions=EXTRACTION_INSTRUCTIONS,
            )

            async def process_record(i: int, raw: dict, extracted) -> RunRecord:
                record = RunRecord(
                    index=batch_start + i,
                    raw_data=raw,
                    extracted_data=extracted.data,
                )
                async with semaphore:
                    result = await self._api_caller.call(
                        spec=api_spec,
                        record_data=extracted.data,
                        dry_run=task.dry_run,
                    )
                record.api_response = result.response_body
                record.http_status_code = result.status_code
                record.retries = result.retries
                record.status = "success" if result.success else "failed"
                record.error = result.error
                return record

            tasks = [
                process_record(i, batch[i], extraction_results[i])
                for i in range(len(batch))
            ]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            for r in results:
                if isinstance(r, Exception):
                    yield RunRecord(
                        index=-1,
                        raw_data={},
                        status="failed",
                        error=str(r),
                    )
                else:
                    yield r
