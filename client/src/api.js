const API_BASE = 'http://localhost:5000/api'

export async function requestRoute(start, end) {
  const response = await fetch(`${API_BASE}/route`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ start, end }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.error || 'Failed to fetch route')
  }

  return data
}
