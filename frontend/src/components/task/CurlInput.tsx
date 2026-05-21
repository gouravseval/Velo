import { useState } from 'react'

function parseCurlPreview(curl: string) {
  try {
    const methodMatch = curl.match(/-X\s+(\w+)/i)
    const urlMatch = curl.match(/https?:\/\/[^\s'"\\]+/)
    const headerMatches = [...curl.matchAll(/-H\s+["']([^"']+)["']/g)]
    const placeholderMatches = [...curl.matchAll(/\{(\w+)\}/g)]

    return {
      method: methodMatch?.[1]?.toUpperCase() ?? 'GET',
      url: urlMatch?.[0] ?? '',
      headers: headerMatches.map((m) => m[1].split(':')[0].trim()),
      placeholders: [...new Set(placeholderMatches.map((m) => m[1]))],
    }
  } catch {
    return null
  }
}

interface Props {
  value: string
  onChange: (v: string) => void
}

const PLACEHOLDER_EXAMPLE = 'Enter Curl'

export function CurlInput({ value, onChange }: Props) {
  const [showPreview, setShowPreview] = useState(false)
  const preview = value ? parseCurlPreview(value) : null

  return (
    <div className="form-group">
      <label className="form-label" htmlFor="curl-input">
        API Curl Command
      </label>
      <div className="text-xs text-secondary" style={{ marginBottom: 8 }}>
        Paste your curl command. Use <span className="placeholder-tag">{'{field}'}</span> placeholders — they'll be filled per record.
      </div>
      <textarea
        id="curl-input"
        className="form-control"
        style={{ minHeight: 140 }}
        value={value}
        onChange={(e) => onChange(e.target.value)}
        placeholder={PLACEHOLDER_EXAMPLE}
        spellCheck={false}
        autoComplete="off"
      />
      {value && (
        <button
          type="button"
          className="btn btn-ghost btn-sm mt-2"
          onClick={() => setShowPreview(!showPreview)}
        >
          {showPreview ? '▲ Hide' : '▼ Show'} parsed preview
        </button>
      )}
      {showPreview && preview && (
        <div className="curl-preview fade-in">
          <div className="curl-preview-row">
            <span className="curl-preview-label">Method</span>
            <span className="curl-preview-value">{preview.method}</span>
          </div>
          {preview.url && (
            <div className="curl-preview-row">
              <span className="curl-preview-label">URL</span>
              <span className="curl-preview-value">{preview.url}</span>
            </div>
          )}
          {preview.headers.length > 0 && (
            <div className="curl-preview-row">
              <span className="curl-preview-label">Headers</span>
              <span className="curl-preview-value">{preview.headers.join(', ')}</span>
            </div>
          )}
          {preview.placeholders.length > 0 && (
            <div className="curl-preview-row">
              <span className="curl-preview-label">Fill vars</span>
              <span style={{ display: 'flex', flexWrap: 'wrap', gap: 4 }}>
                {preview.placeholders.map((p) => (
                  <span key={p} className="placeholder-tag">{`{${p}}`}</span>
                ))}
              </span>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
