import { create } from 'zustand'
import { immer } from 'zustand/middleware/immer'
import type { SseEvent } from '@/types/sse'
import type { RunRecord, RunStatus } from '@/types/run'

export interface RunState {
  runId: string | null
  status: RunStatus
  totalRecords: number
  processedRecords: number
  successCount: number
  failedCount: number
  records: RunRecord[]
  isStreaming: boolean
  errorMessage: string | null
}

interface RunStore extends RunState {
  startRun: (runId: string) => void
  applyEvent: (event: SseEvent) => void
  reset: () => void
}

const initialState: RunState = {
  runId: null,
  status: 'idle',
  totalRecords: 0,
  processedRecords: 0,
  successCount: 0,
  failedCount: 0,
  records: [],
  isStreaming: false,
  errorMessage: null,
}

export const useRunStore = create<RunStore>()(
  immer((set) => ({
    ...initialState,

    startRun: (runId) =>
      set((state) => {
        Object.assign(state, { ...initialState, runId, isStreaming: true, status: 'pending' })
      }),

    applyEvent: (event) =>
      set((state) => {
        switch (event.type) {
          case 'status':
            state.status = event.status as RunStatus
            break
          case 'record':
            state.processedRecords += 1
            if (event.status === 'success') state.successCount += 1
            if (event.status === 'failed') state.failedCount += 1
            state.records.push({
              index: event.index,
              status: event.status,
              extracted_data: event.extracted,
              http_status_code: event.http_status,
              error: event.error,
            })
            break
          case 'completed':
            state.status = 'completed'
            state.totalRecords = event.total
            state.isStreaming = false
            break
          case 'error':
            state.status = 'failed'
            state.isStreaming = false
            state.errorMessage =
              'message' in event ? (event.message ?? null) : (event.errors?.join('; ') ?? null)
            break
          case 'timeout':
            state.isStreaming = false
            break
        }
      }),

    reset: () => set(() => ({ ...initialState })),
  }))
)
