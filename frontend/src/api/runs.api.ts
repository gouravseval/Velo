import { apiClient } from './client'
import type { Run } from '@/types/run'

export const runsApi = {
  get: async (runId: string): Promise<Run> => {
    const res = await apiClient.get(`/api/v1/runs/${runId}`)
    return res.data
  },
}
