export type RunStatus =
  | 'pending'
  | 'extracting'
  | 'calling_api'
  | 'completed'
  | 'failed'
  | 'cancelled'
  | 'idle'

export interface RunRecord {
  index: number
  status: 'pending' | 'success' | 'failed' | 'skipped'
  extracted_data?: Record<string, unknown>
  api_response?: Record<string, unknown>
  http_status_code?: number
  retries?: number
  error?: string
}

export interface Run {
  id: string
  task_id: string
  agent_id: string
  status: RunStatus
  total_records: number
  processed_records: number
  success_count: number
  failed_count: number
  skipped_count: number
  dry_run: boolean
  started_at?: string
  completed_at?: string
  error_message?: string
  records: RunRecord[]
}
