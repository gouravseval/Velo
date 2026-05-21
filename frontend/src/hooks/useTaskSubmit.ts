import { useState, useCallback } from 'react'
import { useNavigate } from 'react-router-dom'
import { tasksApi } from '@/api/tasks.api'
import { useRunStore } from '@/store/runStore'

export function useTaskSubmit() {
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const startRun = useRunStore((s) => s.startRun)
  const navigate = useNavigate()

  const submit = useCallback(
    async (params: {
      agentId: string
      file: File
      curlCommand: string
      dryRun: boolean
      concurrency: number
    }) => {
      setLoading(true)
      setError(null)
      try {
        const formData = new FormData()
        formData.append('agent_id', params.agentId)
        formData.append('file', params.file)
        formData.append('curl_command', params.curlCommand)
        formData.append('dry_run', String(params.dryRun))
        formData.append('concurrency', String(params.concurrency))

        const { run_id } = await tasksApi.create(formData)
        startRun(run_id)
        navigate(`/runs/${run_id}`)
      } catch (e: unknown) {
        setError(e instanceof Error ? e.message : 'Unknown error occurred')
      } finally {
        setLoading(false)
      }
    },
    [startRun, navigate]
  )

  return { submit, loading, error }
}
