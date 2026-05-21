from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from app.infrastructure.streaming.sse_event_bus import SseEventBus
from app.api.dependencies import get_event_bus

router = APIRouter(prefix="/runs", tags=["stream"])


@router.get("/{run_id}/stream")
async def stream_run(
    run_id: str,
    event_bus: SseEventBus = Depends(get_event_bus),
):
    return StreamingResponse(
        event_bus.subscribe(run_id),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
        },
    )
