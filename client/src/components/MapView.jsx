import { MapContainer, TileLayer, Marker, Polyline, useMapEvents } from 'react-leaflet'
import L from 'leaflet'
import icon from 'leaflet/dist/images/marker-icon.png'
import iconShadow from 'leaflet/dist/images/marker-shadow.png'

// Vite doesn't resolve Leaflet's default marker image paths automatically.
const DefaultIcon = L.icon({
  iconUrl: icon,
  shadowUrl: iconShadow,
  iconAnchor: [12, 41],
})
L.Marker.prototype.options.icon = DefaultIcon

const PHILADELPHIA_CENTER = [39.9526, -75.1652]

function ClickHandler({ onMapClick }) {
  useMapEvents({
    click(e) {
      onMapClick([e.latlng.lat, e.latlng.lng])
    },
  })
  return null
}

function MapView({ origin, destination, routeGeometry, onMapClick }) {
  return (
    <MapContainer center={PHILADELPHIA_CENTER} zoom={13} style={{ height: '500px', width: '100%' }}>
      <TileLayer
        attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
      />
      <ClickHandler onMapClick={onMapClick} />
      {origin && <Marker position={origin} />}
      {destination && <Marker position={destination} />}
      {routeGeometry && <Polyline positions={routeGeometry} />}
    </MapContainer>
  )
}

export default MapView
