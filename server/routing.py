import json
import logging
import math
from pathlib import Path

import requests

from config import Config

ORS_DIRECTIONS_URL = "https://api.openrouteservice.org/v2/directions/{profile}/geojson"
FIXTURE_PATH = Path(__file__).parent / "fixtures" / "sample_route.json"


def get_route(start, end, profile="cycling-regular"):
    """start/end are [lat, lng]. Calls Openrouteservice and returns a normalized route dict."""
    if not Config.ORS_API_KEY:
        logging.warning(
            "ORS_API_KEY not set; serving the bundled fixture route instead of calling Openrouteservice."
        )
        return _load_fixture()

    url = ORS_DIRECTIONS_URL.format(profile=profile)
    headers = {
        "Authorization": Config.ORS_API_KEY,
        "Content-Type": "application/json",
    }
    body = {
        "coordinates": [[start[1], start[0]], [end[1], end[0]]],
        "elevation": True,
    }

    response = requests.post(url, json=body, headers=headers, timeout=10)
    response.raise_for_status()
    return normalize_response(response.json())


def _load_fixture():
    with open(FIXTURE_PATH) as f:
        return json.load(f)


def normalize_response(data):
    feature = data["features"][0]
    properties = feature["properties"]
    raw_coords = feature["geometry"]["coordinates"]

    geometry = [[lat, lng] for lng, lat, *_ in raw_coords]
    elevations_m = [coord[2] for coord in raw_coords]
    distances_m = _cumulative_distances(geometry)

    elevation = [
        {"distance_m": round(d, 1), "elevation_m": round(e, 1)}
        for d, e in zip(distances_m, elevations_m)
    ]

    return {
        "geometry": geometry,
        "elevation": elevation,
        "distance_m": round(properties["summary"]["distance"], 1),
        "duration_s": round(properties["summary"]["duration"], 1),
        "ascent_m": round(properties.get("ascent", 0), 1),
        "descent_m": round(properties.get("descent", 0), 1),
    }


def _cumulative_distances(geometry):
    distances = [0.0]
    for i in range(1, len(geometry)):
        distances.append(distances[-1] + _haversine_m(geometry[i - 1], geometry[i]))
    return distances


def _haversine_m(p1, p2):
    radius = 6371000
    lat1, lng1 = math.radians(p1[0]), math.radians(p1[1])
    lat2, lng2 = math.radians(p2[0]), math.radians(p2[1])
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlng / 2) ** 2
    return 2 * radius * math.asin(math.sqrt(a))
