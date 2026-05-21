import { apiClient } from './client'

export const tasksApi = {
  create: async (formData: FormData): Promise<{ run_id: string; status: string }> => {
    const res = await apiClient.post('/api/v1/tasks/', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    return res.data
  },
}
