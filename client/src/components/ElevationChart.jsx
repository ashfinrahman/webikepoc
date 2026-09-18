import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer } from 'recharts'

function ElevationChart({ elevation }) {
  return (
    <ResponsiveContainer width="100%" height={200}>
      <AreaChart data={elevation}>
        <XAxis dataKey="distance_m" tickFormatter={(m) => `${(m / 1000).toFixed(1)} km`} />
        <YAxis unit="m" />
        <Tooltip
          formatter={(value) => `${value} m`}
          labelFormatter={(m) => `${(m / 1000).toFixed(2)} km`}
        />
        <Area type="monotone" dataKey="elevation_m" stroke="#2563eb" fill="#93c5fd" />
      </AreaChart>
    </ResponsiveContainer>
  )
}

export default ElevationChart
