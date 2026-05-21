export type SseEventType = 'status' | 'record' | 'completed' | 'error' | 'timeout'

export interface SseStatusEvent {
  type: 'status'
  status: string
}

export interface SseRecordEvent {
  type: 'record'
  index: number
  status: 'success' | 'failed' | 'skipped'
  extracted?: Record<string, unknown>
  http_status?: number
  error?: string
}

export interface SseCompletedEvent {
  type: 'completed'
  total: number
  success: number
  failed: number
}

export interface SseErrorEvent {
  type: 'error'
  message?: string
  errors?: string[]
}

export type SseEvent =
  | SseStatusEvent
  | SseRecordEvent
  | SseCompletedEvent
  | SseErrorEvent
  | { type: 'timeout' }
