import { useState } from 'react'
import MapView from './components/MapView'

function App() {
  const [origin, setOrigin] = useState(null)
  const [destination, setDestination] = useState(null)

  function handleMapClick(latlng) {
    if (!origin) {
      setOrigin(latlng)
    } else if (!destination) {
      setDestination(latlng)
    } else {
      setOrigin(latlng)
      setDestination(null)
    }
  }

  return (
    <div>
      <h1>WeBike POC</h1>
      <MapView origin={origin} destination={destination} onMapClick={handleMapClick} />
    </div>
  )
}

export default App
