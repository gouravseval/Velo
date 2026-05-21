import asyncio
import uuid
from datetime import datetime
from app.domain.entities.task import Task
from app.domain.entities.run import Run, RunStatus
from app.domain.interfaces.i_run_repository import IRunRepository
from app.application.services.agent_registry import AgentRegistry
from app.infrastructure.streaming.sse_event_bus import SseEventBus
from app.infrastructure.extractors.llm_extractor import LLMExtractor
from app.infrastructure.http.api_caller import ApiCaller
from app.infrastructure.http.curl_parser import CurlParser
from app.infrastructure.parsers.parser_factory import ParserFactory


class ExecuteRunUseCase:
    """
    Orchestrates the full lifecycle of a task run.

    Single Responsibility: coordinate, never directly parse/call APIs.
    Depends on interfaces, not concrete classes (DIP).
    """

    def __init__(
        self,
        registry: AgentRegistry,
        run_repo: IRunRepository,
        event_bus: SseEventBus,
        extractor: LLMExtractor,
        api_caller: ApiCaller,
        parser_factory: ParserFactory,
        curl_parser: CurlParser,
    ):
        self._registry = registry
        self._run_repo = run_repo
        self._event_bus = event_bus
        self._extractor = extractor
        self._api_caller = api_caller
        self._parser_factory = parser_factory
        self._curl_parser = curl_parser

    async def execute(self, task: Task) -> Run:
        run_id = str(uuid.uuid4())
        run = Run(
            id=run_id,
            task_id=task.id,
            agent_id=task.agent_id,
            started_at=datetime.utcnow(),
            dry_run=task.dry_run,
        )
        await self._run_repo.save(run)

        # Fire and forget — returns run immediately
        asyncio.create_task(self._run_agent(task, run))
        return run

    async def _run_agent(self, task: Task, run: Run) -> None:
        try:
            agent = self._registry.instantiate(
                task.agent_id,
                extractor=self._extractor,
                api_caller=self._api_caller,
                parser_factory=self._parser_factory,
                curl_parser=self._curl_parser,
            )

            # Validation phase
            errors = await agent.validate_task(task)
            if errors:
                run.status = RunStatus.FAILED
                run.error_message = "; ".join(errors)
                await self._run_repo.save(run)
                await self._event_bus.publish(run.id, {"type": "error", "errors": errors})
                return

            run.status = RunStatus.EXTRACTING
            await self._run_repo.save(run)
            await self._event_bus.publish(run.id, {"type": "status", "status": "extracting"})

            # Stream records from agent
            async for record in agent.execute(task, run):
                run.records.append(record)
                run.processed_records += 1
                if record.status == "success":
                    run.success_count += 1
                elif record.status == "failed":
                    run.failed_count += 1
                elif record.status == "skipped":
                    run.skipped_count += 1

                await self._run_repo.save(run)
                await self._event_bus.publish(run.id, {
                    "type": "record",
                    "index": record.index,
                    "status": record.status,
                    "extracted": record.extracted_data,
                    "http_status": record.http_status_code,
                    "error": record.error,
                })

            run.status = RunStatus.COMPLETED
            run.completed_at = datetime.utcnow()
            await self._run_repo.save(run)
            await self._event_bus.publish(run.id, {
                "type": "completed",
                "total": run.total_records,
                "success": run.success_count,
                "failed": run.failed_count,
            })

        except Exception as exc:
            run.status = RunStatus.FAILED
            run.error_message = str(exc)
            run.completed_at = datetime.utcnow()
            await self._run_repo.save(run)
            await self._event_bus.publish(run.id, {"type": "error", "message": str(exc)})
