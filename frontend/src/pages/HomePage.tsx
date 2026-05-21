import { useState } from 'react'
import type { AgentMetadata } from '@/types/agent'
import { AgentCard } from '@/components/agents/AgentCard'
import { TaskForm } from '@/components/task/TaskForm'
import { useAgents } from '@/hooks/useAgents'

export function HomePage() {
  const { agents, loading, error } = useAgents()
  const [selected, setSelected] = useState<AgentMetadata | null>(null)

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', paddingTop: 80 }}>
        <div className="spinner spinner-lg" style={{ marginBottom: 16 }} />
        <div className="text-secondary">Connecting to backend…</div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="alert alert-danger fade-in" style={{ marginTop: 40 }}>
        <span>⚠️</span>
        <div>
          <div className="font-bold">Backend unreachable</div>
          <div className="text-sm">{error}</div>
          <div className="text-xs text-muted" style={{ marginTop: 6 }}>
            Make sure the FastAPI server is running: <code>uvicorn app.main:app --reload</code>
          </div>
        </div>
      </div>
    )
  }

  if (selected !== null) {
    return <TaskForm agent={selected} onBack={() => setSelected(null)} />
  }

  return (
    <div className="fade-in">
      <h1 className="page-title">API Executor <span style={{ color: 'var(--accent)' }}>with File Data</span></h1>
      <p className="page-subtitle">
        Upload a CSV, Excel, or JSON file — we extract each record with AI and call your API automatically, row by row.
      </p>

      {agents.length === 0 ? (
        <div className="empty-state">
          <div className="empty-state-icon">🤖</div>
          <div className="empty-state-title">No agents available</div>
          <div className="empty-state-desc">
            Make sure the backend is running and agents are in <code>app/agents/</code>
          </div>
        </div>
      ) : (
        <div className="agent-grid">
          {agents.map((agent) => (
            <AgentCard
              key={agent.id}
              agent={agent}
              selected={selected !== null && (selected as AgentMetadata).id === agent.id}
              onClick={() => setSelected(agent)}
            />
          ))}
        </div>
      )}
    </div>
  )
}
