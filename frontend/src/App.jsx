import { useState, useEffect, useRef } from 'react'

function App() {
  const [text, setText] = useState('')
  const [result, setResult] = useState('')
  const [status, setStatus] = useState('idle')
  const ws = useRef(null)

  const handleSubmit = async () => {
    setStatus('processing')
    setResult('')

    // POST to job-service
    const response = await fetch('http://localhost:8000/api/job?text=' + encodeURIComponent(text), {
      method: 'POST'
    })
    const data = await response.json()
    const jobId = data.job_id

    // open WebSocket and register job_id
    ws.current = new WebSocket('ws://localhost:8002/ws')
    ws.current.onopen = () => {
      ws.current.send(jobId)
    }
    ws.current.onmessage = (event) => {
      setResult(event.data)
      setStatus('done')
      ws.current.close()
    }
  }

  return (
    <div style={{ maxWidth: 600, margin: '40px auto', fontFamily: 'sans-serif' }}>
      <h1>Text Summarizer</h1>
      <textarea
        rows={8}
        style={{ width: '100%', padding: 8 }}
        value={text}
        onChange={e => setText(e.target.value)}
        placeholder="Paste text here..."
      />
      <button
        onClick={handleSubmit}
        disabled={status === 'processing'}
        style={{ marginTop: 8, padding: '8px 16px' }}
      >
        {status === 'processing' ? 'Processing...' : 'Summarize'}
      </button>
      {result && (
        <div style={{ marginTop: 24 }}>
          <h3>Summary:</h3>
          <p>{result}</p>
        </div>
      )}
    </div>
  )
}

export default App