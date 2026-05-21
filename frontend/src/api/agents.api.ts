import { apiClient } from './client'
import type { AgentMetadata } from '@/types/agent'

export const agentsApi = {
  list: async (): Promise<AgentMetadata[]> => {
    const res = await apiClient.get('/api/v1/agents/')
    return res.data
  },
}
