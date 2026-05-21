interface Props {
  total: number
  processed: number
  success: number
  failed: number
  isStreaming: boolean
}

export function RunProgress({ total, processed, success, failed, isStreaming }: Props) {
  const pct = total > 0 ? Math.round((processed / total) * 100) : 0
  const skipped = processed - success - failed

  return (
    <div>
      <div className="stats-row">
        <div className="stat-card">
          <div className="stat-value">{total || '?'}</div>
          <div className="stat-label">Total</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: 'var(--text-primary)' }}>{processed}</div>
          <div className="stat-label">Processed</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: 'var(--success)' }}>{success}</div>
          <div className="stat-label">Success</div>
        </div>
        <div className="stat-card">
          <div className="stat-value" style={{ color: 'var(--danger)' }}>{failed}</div>
          <div className="stat-label">Failed</div>
        </div>
      </div>

      <div style={{ marginBottom: 8, display: 'flex', justifyContent: 'space-between', fontSize: 13 }}>
        <span className="text-secondary">{isStreaming ? 'Processing…' : 'Complete'}</span>
        <span className="font-bold text-accent">{pct}%</span>
      </div>
      <div className="progress-bar">
        <div
          className={`progress-fill ${isStreaming ? 'animated' : ''}`}
          style={{ width: `${pct}%` }}
        />
      </div>
    </div>
  )
}
