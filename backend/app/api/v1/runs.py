from fastapi import APIRouter, Depends, HTTPException
from app.application.use_cases.get_run_status import GetRunStatusUseCase
from app.api.dependencies import get_run_status_use_case

router = APIRouter(prefix="/runs", tags=["runs"])


@router.get("/{run_id}")
async def get_run(
    run_id: str,
    use_case: GetRunStatusUseCase = Depends(get_run_status_use_case),
):
    run = await use_case.execute(run_id)
    if not run:
        raise HTTPException(status_code=404, detail=f"Run '{run_id}' not found")
    return {
        "id": run.id,
        "task_id": run.task_id,
        "agent_id": run.agent_id,
        "status": run.status,
        "total_records": run.total_records,
        "processed_records": run.processed_records,
        "success_count": run.success_count,
        "failed_count": run.failed_count,
        "skipped_count": run.skipped_count,
        "dry_run": run.dry_run,
        "started_at": run.started_at.isoformat() if run.started_at else None,
        "completed_at": run.completed_at.isoformat() if run.completed_at else None,
        "error_message": run.error_message,
        "records": [
            {
                "index": r.index,
                "status": r.status,
                "extracted_data": r.extracted_data,
                "api_response": r.api_response,
                "http_status_code": r.http_status_code,
                "retries": r.retries,
                "error": r.error,
            }
            for r in run.records
        ],
    }
