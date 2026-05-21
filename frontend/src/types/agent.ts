export interface AgentMetadata {
  id: string
  name: string
  description: string
  version: string
  input_file_types: string[]
  required_api_fields: string[]
  supports_dry_run: boolean
  max_concurrency: number
}
