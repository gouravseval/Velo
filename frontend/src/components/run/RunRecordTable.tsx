import type { RunRecord } from '@/types/run'

const STATUS_CONFIG = {
  success: { label: 'Success', cls: 'badge-success', dot: 'success' },
  failed:  { label: 'Failed',  cls: 'badge-danger',  dot: 'failed' },
  skipped: { label: 'Skipped', cls: 'badge-warning',  dot: 'pending' },
  pending: { label: 'Pending', cls: 'badge-default',  dot: 'pending' },
}

interface Props {
  records: RunRecord[]
}

export function RunRecordTable({ records }: Props) {
  if (records.length === 0) {
    return (
      <div className="empty-state">
        <div className="empty-state-icon">⏳</div>
        <div className="empty-state-title">Waiting for records…</div>
        <div className="empty-state-desc">Results will appear here as each record is processed.</div>
      </div>
    )
  }

  return (
    <div style={{ overflowX: 'auto' }}>
      <table className="data-table">
        <thead>
          <tr>
            <th>#</th>
            <th>Status</th>
            <th>HTTP</th>
            <th>Extracted Data</th>
            <th>Error</th>
          </tr>
        </thead>
        <tbody>
          {records.map((r) => {
            const cfg = STATUS_CONFIG[r.status] ?? STATUS_CONFIG.pending
            return (
              <tr key={`${r.index}-${r.status}`} className="slide-in">
                <td className="font-mono text-xs">{r.index}</td>
                <td>
                  <span className={`badge ${cfg.cls}`}>
                    <span className={`status-dot ${cfg.dot}`} style={{ width: 6, height: 6 }} />
                    {cfg.label}
                  </span>
                </td>
                <td className="font-mono text-xs">
                  {r.http_status_code != null
                    ? <span style={{ color: r.http_status_code < 400 ? 'var(--success)' : 'var(--danger)' }}>{r.http_status_code}</span>
                    : <span className="text-muted">—</span>
                  }
                </td>
                <td className="text-xs font-mono" style={{ maxWidth: 320, wordBreak: 'break-word' }}>
                  {r.extracted_data
                    ? JSON.stringify(r.extracted_data).slice(0, 180)
                    : <span className="text-muted">—</span>
                  }
                </td>
                <td className="text-xs" style={{ color: 'var(--danger)', maxWidth: 200, wordBreak: 'break-word' }}>
                  {r.error ?? <span className="text-muted">—</span>}
                </td>
              </tr>
            )
          })}
        </tbody>
      </table>
    </div>
  )
}
