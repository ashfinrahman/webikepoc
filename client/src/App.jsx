import { useState } from 'react'
import MapView from './components/MapView'
import ElevationChart from './components/ElevationChart'
import { requestRoute } from './api'

function App() {
  const [origin, setOrigin] = useState(null)
  const [destination, setDestination] = useState(null)
  const [route, setRoute] = useState(null)

  async function handleMapClick(latlng) {
    if (!origin) {
      setOrigin(latlng)
    } else if (!destination) {
      setDestination(latlng)
      const result = await requestRoute(origin, latlng)
      setRoute(result)
    } else {
      setOrigin(latlng)
      setDestination(null)
      setRoute(null)
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
