import asyncio
import json
from collections import defaultdict


class SseEventBus:
    """
    In-process pub/sub for SSE streaming.
    Each run_id has a queue of events.
    Consumers await events via subscribe().
    """

    def __init__(self):
        self._queues: dict[str, list[asyncio.Queue]] = defaultdict(list)

    async def publish(self, run_id: str, event: dict) -> None:
        for q in self._queues.get(run_id, []):
            await q.put(event)

    async def subscribe(self, run_id: str):
        """AsyncGenerator that yields SSE-formatted strings."""
        queue: asyncio.Queue = asyncio.Queue()
        self._queues[run_id].append(queue)
        try:
            while True:
                event = await asyncio.wait_for(queue.get(), timeout=60.0)
                yield f"data: {json.dumps(event)}\n\n"
                if event.get("type") in ("completed", "error"):
                    break
        except asyncio.TimeoutError:
            yield f"data: {json.dumps({'type': 'timeout'})}\n\n"
        finally:
            if queue in self._queues[run_id]:
                self._queues[run_id].remove(queue)
            if not self._queues[run_id]:
                del self._queues[run_id]
