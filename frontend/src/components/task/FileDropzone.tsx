import { useRef, useState } from 'react'

interface Props {
  file: File | null
  onChange: (f: File | null) => void
  accept?: string
}

function formatBytes(bytes: number) {
  if (bytes < 1024) return `${bytes} B`
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`
}

export function FileDropzone({ file, onChange, accept = '.csv,.xlsx,.json' }: Props) {
  const inputRef = useRef<HTMLInputElement>(null)
  const [dragging, setDragging] = useState(false)

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault()
    setDragging(false)
    const f = e.dataTransfer.files[0]
    if (f) onChange(f)
  }

  if (file) {
    return (
      <div className="dropzone-file">
        <div className="dropzone-file-icon">📄</div>
        <div style={{ flex: 1 }}>
          <div className="dropzone-file-name">{file.name}</div>
          <div className="dropzone-file-size">{formatBytes(file.size)}</div>
        </div>
        <button
          type="button"
          className="btn btn-ghost btn-sm"
          onClick={() => onChange(null)}
        >
          ✕ Remove
        </button>
      </div>
    )
  }

  return (
    <div
      className={`dropzone ${dragging ? 'drag-over' : ''}`}
      onDragOver={(e) => { e.preventDefault(); setDragging(true) }}
      onDragLeave={() => setDragging(false)}
      onDrop={handleDrop}
      onClick={() => inputRef.current?.click()}
    >
      <input
        ref={inputRef}
        type="file"
        accept={accept}
        style={{ display: 'none' }}
        onChange={(e) => onChange(e.target.files?.[0] ?? null)}
        id="file-dropzone-input"
      />
      <div className="dropzone-icon">📂</div>
      <div className="dropzone-text">Drop your file here or click to browse</div>
      <div className="dropzone-hint">Supports CSV, Excel (.xlsx), and JSON</div>
    </div>
  )
}
