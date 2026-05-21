import { useState } from 'react'
import type { AgentMetadata } from '@/types/agent'
import { FileDropzone } from './FileDropzone'
import { CurlInput } from './CurlInput'
import { useTaskSubmit } from '@/hooks/useTaskSubmit'
import { getAgentIcon } from '@/utils/agentIcon'

interface Props {
  agent: AgentMetadata
  onBack: () => void
}

export function TaskForm({ agent, onBack }: Props) {
  const icon = getAgentIcon(agent)
  const [file, setFile] = useState<File | null>(null)
  const [curl, setCurl] = useState('')
  const [dryRun, setDryRun] = useState(false)
  const [concurrency, setConcurrency] = useState(3)
  const { submit, loading, error } = useTaskSubmit()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!file || !curl.trim()) return
    await submit({ agentId: agent.id, file, curlCommand: curl, dryRun, concurrency })
  }

  const valid = !!file && curl.trim().length > 0

  return (
    <form onSubmit={handleSubmit} className="fade-in">
      {/* Agent info banner */}
      <div className="card" style={{ marginBottom: 24, background: 'var(--accent-dim)', borderColor: 'var(--border-accent)' }}>
        <div className="flex items-center gap-3">
          <div className="agent-icon" style={{ marginBottom: 0 }}>{icon}</div>
          <div>
            <div className="font-bold" style={{ fontSize: 16 }}>{agent.name}</div>
            <div className="text-sm text-secondary">{agent.description}</div>
          </div>
          <button type="button" className="btn btn-ghost btn-sm" style={{ marginLeft: 'auto' }} onClick={onBack}>
            ← Back
          </button>
        </div>
      </div>

      {/* File upload */}
      <div className="card" style={{ marginBottom: 16 }}>
        <h3 className="font-bold" style={{ marginBottom: 16, fontSize: 15 }}>1. Upload Data File</h3>
        <FileDropzone file={file} onChange={setFile} />
      </div>

      {/* Curl command */}
      <div className="card" style={{ marginBottom: 16 }}>
        <h3 className="font-bold" style={{ marginBottom: 16, fontSize: 15 }}>2. Configure API</h3>
        <CurlInput value={curl} onChange={setCurl} />
      </div>

      {/* Options */}
      <div className="card" style={{ marginBottom: 24 }}>
        <h3 className="font-bold" style={{ marginBottom: 16, fontSize: 15 }}>3. Run Options</h3>
        <div className="flex gap-4" style={{ flexWrap: 'wrap' }}>
          <div style={{ flex: 1, minWidth: 180 }}>
            <label className="form-label" htmlFor="concurrency-input">Concurrency</label>
            <input
              id="concurrency-input"
              type="number"
              className="form-control"
              min={1} max={10}
              value={concurrency}
              onChange={(e) => setConcurrency(Number(e.target.value))}
            />
            <div className="text-xs text-muted mt-2">Parallel API calls per batch (1–10)</div>
          </div>
          <div style={{ flex: 1, minWidth: 180 }}>
            <div className="form-label">Dry Run</div>
            <div
              className="toggle-wrapper"
              onClick={() => setDryRun(!dryRun)}
              style={{ marginTop: 8 }}
            >
              <div className={`toggle ${dryRun ? 'on' : ''}`} id="dry-run-toggle">
                <div className="toggle-knob" />
              </div>
              <span className="text-sm" style={{ color: dryRun ? 'var(--accent)' : 'var(--text-secondary)' }}>
                {dryRun ? 'Enabled — no real API calls' : 'Disabled'}
              </span>
            </div>
          </div>
        </div>
      </div>

      {error && (
        <div className="alert alert-danger" style={{ marginBottom: 16 }}>
          <span>⚠️</span> {error}
        </div>
      )}

      <button
        type="submit"
        className="btn btn-primary btn-lg w-full"
        id="run-agent-btn"
        disabled={!valid || loading}
      >
        {loading ? (
          <>
            <div className="spinner" />
            Starting Run…
          </>
        ) : (
          <>⚡ Run Agent</>
        )}
      </button>
    </form>
  )
}
