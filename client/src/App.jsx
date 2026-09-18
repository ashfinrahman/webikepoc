import { useState } from 'react'
import MapView from './components/MapView'
import ElevationChart from './components/ElevationChart'
import { requestRoute } from './api'

function App() {
  const [origin, setOrigin] = useState(null)
  const [destination, setDestination] = useState(null)
  const [route, setRoute] = useState(null)
  const [error, setError] = useState(null)

  async function handleMapClick(latlng) {
    if (!origin) {
      setOrigin(latlng)
      setError(null)
    } else if (!destination) {
      setDestination(latlng)
      try {
        const result = await requestRoute(origin, latlng)
        setRoute(result)
        setError(null)
      } catch (err) {
        setError(err.message)
        setRoute(null)
      }
    } else {
      setOrigin(latlng)
      setDestination(null)
      setRoute(null)
      setError(null)
    }
  }

  return (
    <div>
      <h1>WeBike POC</h1>
      <MapView
        origin={origin}
        destination={destination}
        routeGeometry={route?.geometry}
        onMapClick={handleMapClick}
      />
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {route && (
        <div>
          <p>
            {(route.distance_m / 1000).toFixed(2)} km · {(route.duration_s / 60).toFixed(0)} min ·
            +{route.ascent_m.toFixed(0)} m / -{route.descent_m.toFixed(0)} m
          </p>
          <ElevationChart elevation={route.elevation} />
        </div>
      )}
    </div>
  )
}

export default App
