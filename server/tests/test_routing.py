import json
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

import routing
from app import create_app
from config import Config

FIXTURE_PATH = Path(__file__).resolve().parent.parent / "fixtures" / "sample_route.json"

RAW_ORS_RESPONSE = {
    "features": [
        {
            "properties": {
                "summary": {"distance": 1200.5, "duration": 300.2},
                "ascent": 15.0,
                "descent": 8.0,
            },
            "geometry": {
                "coordinates": [
                    [-75.1652, 39.9526, 30.0],
                    [-75.1600, 39.9520, 28.0],
                    [-75.1550, 39.9510, 25.0],
                ]
            },
        }
    ]
}


def test_normalize_response_flips_coords_and_computes_distance():
    result = routing.normalize_response(RAW_ORS_RESPONSE)

    assert result["geometry"][0] == [39.9526, -75.1652]
    assert len(result["geometry"]) == 3
    assert len(result["elevation"]) == 3
    assert result["elevation"][0] == {"distance_m": 0.0, "elevation_m": 30.0}
    assert result["distance_m"] == 1200.5
    assert result["duration_s"] == 300.2
    assert result["ascent_m"] == 15.0
    assert result["descent_m"] == 8.0


def test_get_route_falls_back_to_fixture_when_no_api_key(monkeypatch):
    monkeypatch.setattr(Config, "ORS_API_KEY", "")

    with open(FIXTURE_PATH) as f:
        expected = json.load(f)

    result = routing.get_route([39.9526, -75.1652], [39.9469, -75.1352])

    assert result == expected


def test_get_route_calls_ors_when_api_key_present(monkeypatch):
    monkeypatch.setattr(Config, "ORS_API_KEY", "test-key")

    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = RAW_ORS_RESPONSE

    with patch("routing.requests.post", return_value=mock_response) as mock_post:
        result = routing.get_route([39.9526, -75.1652], [39.9510, -75.1550])

    mock_post.assert_called_once()
    assert result["distance_m"] == 1200.5


@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as test_client:
        yield test_client


def test_post_route_happy_path(monkeypatch, client):
    monkeypatch.setattr(Config, "ORS_API_KEY", "")  # forces the fixture, no network

    response = client.post(
        "/api/route", json={"start": [39.9526, -75.1652], "end": [39.9469, -75.1352]}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "geometry" in data
    assert "elevation" in data
    assert data["distance_m"] > 0


def test_post_route_invalid_coordinates(client):
    response = client.post("/api/route", json={"start": "nope", "end": [39.9469, -75.1352]})

    assert response.status_code == 400
    assert "error" in response.get_json()
