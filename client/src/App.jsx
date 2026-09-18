import { useState } from 'react'
import MapView from './components/MapView'
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
    </div>
  )
}

export default App
