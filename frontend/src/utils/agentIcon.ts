/**
 * Shared utility — derive a generic emoji icon from an agent's metadata.
 * No hardcoded IDs. Works for any agent the backend discovers.
 */

const FILE_TYPE_ICONS: Record<string, string> = {
  csv:  '📊',
  xlsx: '📊',
  json: '📋',
  xml:  '📄',
  pdf:  '📕',
}

const KEYWORD_ICONS: [RegExp, string][] = [
  [/email|mail|smtp/i,         '📧'],
  [/rating|review|star/i,      '⭐'],
  [/product|inventory|stock/i, '📦'],
  [/user|customer|person/i,    '👤'],
  [/payment|invoice|billing/i, '💳'],
  [/sms|message|notify/i,      '💬'],
  [/report|analytics/i,        '📈'],
  [/image|photo|media/i,       '🖼️'],
  [/order|shipment|delivery/i, '🚚'],
  [/sync|update|import/i,      '🔄'],
]

/**
 * Returns an emoji icon for any agent — no hardcoded IDs.
 * Priority: keyword match on name/description → primary file type → fallback
 */
export function getAgentIcon(agent: { name: string; description: string; input_file_types: string[] }): string {
  const text = `${agent.name} ${agent.description}`

  for (const [pattern, icon] of KEYWORD_ICONS) {
    if (pattern.test(text)) return icon
  }

  const primaryType = agent.input_file_types[0]
  if (primaryType && FILE_TYPE_ICONS[primaryType]) {
    return FILE_TYPE_ICONS[primaryType]
  }

  return '🤖'
}
