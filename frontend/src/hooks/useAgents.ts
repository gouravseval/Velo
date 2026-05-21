import { useState, useEffect } from 'react'
import { agentsApi } from '@/api/agents.api'
import type { AgentMetadata } from '@/types/agent'

export function useAgents() {
  const [agents, setAgents] = useState<AgentMetadata[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    agentsApi
      .list()
      .then(setAgents)
      .catch((e) => setError(e.message))
      .finally(() => setLoading(false))
  }, [])

  return { agents, loading, error }
}
