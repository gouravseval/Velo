import type { AgentMetadata } from '@/types/agent'
import { getAgentIcon } from '@/utils/agentIcon'

interface Props {
  agent: AgentMetadata
  selected?: boolean
  onClick: () => void
}

export function AgentCard({ agent, selected, onClick }: Props) {
  const icon = getAgentIcon(agent)

  return (
    <div
      className={`agent-card fade-in ${selected ? 'selected' : ''}`}
      onClick={onClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => e.key === 'Enter' && onClick()}
      id={`agent-card-${agent.id}`}
    >
      <div className="agent-icon">{icon}</div>
      <div className="agent-name">{agent.name}</div>
      <div className="agent-desc">{agent.description}</div>
      <div className="agent-tags">
        {agent.input_file_types.map((t) => (
          <span key={t} className="badge badge-default">.{t}</span>
        ))}
        {agent.supports_dry_run && (
          <span className="badge badge-accent">Dry Run</span>
        )}
        <span className="badge badge-default">v{agent.version}</span>
      </div>
    </div>
  )
}
