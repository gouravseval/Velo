import { Link } from 'react-router-dom'

interface Props {
  total: number
  success: number
  failed: number
}

export function RunReport({ total, success, failed }: Props) {
  const rate = total > 0 ? Math.round((success / total) * 100) : 0

  return (
    <div className="card fade-in" style={{ background: 'var(--success-dim)', borderColor: 'rgba(34,197,94,0.3)' }}>
      <div className="flex items-center gap-3" style={{ marginBottom: 16 }}>
        <span style={{ fontSize: 28 }}>✅</span>
        <div>
          <div className="font-bold" style={{ fontSize: 18, color: 'var(--success)' }}>Run Completed</div>
          <div className="text-sm text-secondary">{rate}% success rate</div>
        </div>
        <Link to="/" className="btn btn-secondary btn-sm" style={{ marginLeft: 'auto' }}>
          ← New Run
        </Link>
      </div>
      <div style={{ display: 'flex', gap: 16 }}>
        <span className="badge badge-success">✓ {success} succeeded</span>
        {failed > 0 && <span className="badge badge-danger">✕ {failed} failed</span>}
        <span className="badge badge-default">{total} total</span>
      </div>
    </div>
  )
}
