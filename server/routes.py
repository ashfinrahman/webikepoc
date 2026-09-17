from flask import Blueprint, jsonify, request

from routing import get_route

api_bp = Blueprint("api", __name__)


@api_bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@api_bp.post("/route")
def create_route():
    payload = request.get_json(force=True)
    route = get_route(payload["start"], payload["end"])
    return jsonify(route)
