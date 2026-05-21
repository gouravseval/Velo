import { useParams, Link } from 'react-router-dom'
import { useRunStore } from '@/store/runStore'
import { useRunStream } from '@/hooks/useRunStream'
import { RunProgress } from '@/components/run/RunProgress'
import { RunRecordTable } from '@/components/run/RunRecordTable'
import { RunReport } from '@/components/run/RunReport'

const STATUS_LABELS: Record<string, { label: string; cls: string; dot: string }> = {
  pending:     { label: 'Pending',     cls: 'badge-default', dot: 'pending' },
  extracting:  { label: 'Extracting',  cls: 'badge-accent',  dot: 'running pulsing' },
  calling_api: { label: 'Calling API', cls: 'badge-accent',  dot: 'running pulsing' },
  completed:   { label: 'Completed',   cls: 'badge-success', dot: 'success' },
  failed:      { label: 'Failed',      cls: 'badge-danger',  dot: 'failed' },
  cancelled:   { label: 'Cancelled',   cls: 'badge-default', dot: 'pending' },
}

export function RunPage() {
  const { runId } = useParams<{ runId: string }>()
  const { status, isStreaming, totalRecords, successCount, failedCount, processedRecords, records, errorMessage } =
    useRunStore()

  useRunStream(runId)

  const statusCfg = STATUS_LABELS[status] ?? { label: status, cls: 'badge-default', dot: 'pending' }

  return (
    <div className="fade-in">
      {/* Page header */}
      <div className="flex items-center justify-between" style={{ marginBottom: 24 }}>
        <div>
          <h1 className="page-title">Live Run</h1>
          <span className="font-mono text-xs text-muted">{runId}</span>
        </div>
        <div className="flex items-center gap-3">
          <span className={`badge ${statusCfg.cls}`}>
            <span className={`status-dot ${statusCfg.dot}`} />
            {statusCfg.label}
          </span>
          <Link to="/" className="btn btn-secondary btn-sm">← Back</Link>
        </div>
      </div>

      {/* Error banner */}
      {errorMessage && (
        <div className="alert alert-danger" style={{ marginBottom: 20 }}>
          <span>⚠️</span> {errorMessage}
        </div>
      )}

      {/* Progress */}
      <div className="card" style={{ marginBottom: 20 }}>
        <RunProgress
          total={totalRecords}
          processed={processedRecords}
          success={successCount}
          failed={failedCount}
          isStreaming={isStreaming}
        />
      </div>

      {/* Completion report */}
      {status === 'completed' && (
        <RunReport total={totalRecords} success={successCount} failed={failedCount} />
      )}

      {/* Record table */}
      <div className="card" style={{ marginTop: 20 }}>
        <div className="flex items-center justify-between" style={{ marginBottom: 16 }}>
          <h2 className="font-bold" style={{ fontSize: 16 }}>Records</h2>
          <span className="badge badge-default">{records.length} so far</span>
        </div>
        <RunRecordTable records={records} />
      </div>
    </div>
  )
}
