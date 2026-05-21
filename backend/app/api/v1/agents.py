from fastapi import APIRouter, Depends
from app.application.use_cases.list_agents import ListAgentsUseCase
from app.api.dependencies import get_list_agents_use_case

router = APIRouter(prefix="/agents", tags=["agents"])


@router.get("/")
async def list_agents(use_case: ListAgentsUseCase = Depends(get_list_agents_use_case)):
    agents = use_case.execute()
    return [
        {
            "id": a.id,
            "name": a.name,
            "description": a.description,
            "version": a.version,
            "input_file_types": a.input_file_types,
            "required_api_fields": a.required_api_fields,
            "supports_dry_run": a.supports_dry_run,
            "max_concurrency": a.max_concurrency,
        }
        for a in agents
    ]
