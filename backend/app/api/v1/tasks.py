import uuid
from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from app.application.use_cases.execute_run import ExecuteRunUseCase
from app.domain.entities.task import Task
from app.api.dependencies import get_execute_run_use_case

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.post("/", status_code=202)
async def create_task(
    agent_id: str = Form(...),
    curl_command: str = Form(...),
    dry_run: bool = Form(False),
    concurrency: int = Form(3),
    file: UploadFile = File(...),
    use_case: ExecuteRunUseCase = Depends(get_execute_run_use_case),
):
    file_bytes = await file.read()
    task = Task(
        id=str(uuid.uuid4()),
        agent_id=agent_id,
        file_bytes=file_bytes,
        file_name=file.filename or "",
        file_content_type=file.content_type or "application/octet-stream",
        curl_command=curl_command,
        dry_run=dry_run,
        concurrency=concurrency,
    )
    run = await use_case.execute(task)
    return {"run_id": run.id, "status": run.status}
