import { MapContainer, TileLayer } from 'react-leaflet'

const PHILADELPHIA_CENTER = [39.9526, -75.1652]

function MapView() {
  return (
    <MapContainer center={PHILADELPHIA_CENTER} zoom={13} style={{ height: '500px', width: '100%' }}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
    </MapContainer>
  )
}

export default MapView
