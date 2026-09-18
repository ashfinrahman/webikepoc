# webike-poc

Proof-of-concept for a cycling-aware navigation stack: a Leaflet map client, a
Flask API, a SQLAlchemy/SQLite database, and the Openrouteservice directions
API for elevation-aware routing.

This is a class exercise, not the full WeBike app — no accounts, no hazard
reporting, no custom route weighting. Just proving the four pieces talk to
each other: click two points on a map, get a cycling route back with an
elevation profile, and see that request persisted server-side.

## Tested on

- Ubuntu 24.04 LTS
- Python 3.12.3
- Node 20.x (npm 10.x)

## Backend setup

```bash
cd server
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

Get a free Openrouteservice API key at https://openrouteservice.org/dev/#/signup
and put it in `.env` as `ORS_API_KEY=...`. **This is optional** — if
`ORS_API_KEY` is left blank, the server logs a warning and serves a bundled
fixture route (`server/fixtures/sample_route.json`) instead of calling the
API, so the whole demo runs with no key and no network access.

Run the API:

```bash
python app.py
```

The server listens on http://localhost:5000. Check it's alive:

```bash
curl http://localhost:5000/api/health
```

Run the tests:

```bash
pytest
```

## Frontend setup

```bash
cd client
npm install
npm run dev
```

Open the printed local URL (usually http://localhost:5173). Click two points
on the map to set an origin and destination; a third click resets and starts
over. The route polyline, a distance/duration/ascent summary, and an
elevation chart appear once the backend responds.

## API

- `GET /api/health` — liveness check.
- `POST /api/route` — body `{"start": [lat, lng], "end": [lat, lng]}`, returns
  the normalized route (geometry, elevation profile, distance, duration,
  ascent, descent) and persists the request. Returns `400` for missing or
  malformed coordinates, `502` if Openrouteservice is unreachable or errors.
- `GET /api/routes` — the last 20 persisted route requests, as JSON. There's
  no UI for this; it exists to prove the SQLAlchemy/SQLite layer works.

## Known issue

`npm audit` flags a moderate advisory in Vite 5's bundled esbuild
(dev-server-only CORS issue, GHSA-67mh-4wv8-2f99). It doesn't affect
production builds, and fixing it requires the Vite 6/7 major version bump,
which is out of scope for this proof of concept.
