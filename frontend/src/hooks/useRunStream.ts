import { useEffect, useRef } from 'react'
import { useRunStore } from '@/store/runStore'
import { API_BASE_URL } from '@/api/client'
import type { SseEvent } from '@/types/sse'

export function useRunStream(runId: string | undefined) {
  const applyEvent = useRunStore((s) => s.applyEvent)
  const eventSourceRef = useRef<EventSource | null>(null)

  useEffect(() => {
    if (!runId) return

    const es = new EventSource(`${API_BASE_URL}/api/v1/runs/${runId}/stream`)
    eventSourceRef.current = es

    es.onmessage = (e) => {
      try {
        const event: SseEvent = JSON.parse(e.data)
        applyEvent(event)
        if (event.type === 'completed' || event.type === 'error') {
          es.close()
        }
      } catch {
        console.warn('Failed to parse SSE event', e.data)
      }
    }

    es.onerror = () => {
      es.close()
    }

    return () => {
      es.close()
    }
  }, [runId, applyEvent])
}
