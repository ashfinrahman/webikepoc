from flask import Blueprint, jsonify, request

from models import RouteRequest, SessionLocal
from routing import RoutingError, get_route

api_bp = Blueprint("api", __name__)


@api_bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@api_bp.post("/route")
def create_route():
    payload = request.get_json(silent=True) or {}
    start = payload.get("start")
    end = payload.get("end")

    if not _is_valid_coord(start) or not _is_valid_coord(end):
        return jsonify({"error": "start and end must both be [lat, lng] pairs of numbers"}), 400

    try:
        route = get_route(start, end)
    except RoutingError as exc:
        return jsonify({"error": str(exc)}), 502

    session = SessionLocal()
    try:
        record = RouteRequest(
            start_lat=start[0],
            start_lng=start[1],
            end_lat=end[0],
            end_lng=end[1],
            profile="cycling-regular",
            distance_m=route["distance_m"],
            duration_s=route["duration_s"],
            ascent_m=route["ascent_m"],
            descent_m=route["descent_m"],
        )
        session.add(record)
        session.commit()
    finally:
        session.close()

    return jsonify(route)


@api_bp.get("/routes")
def list_routes():
    session = SessionLocal()
    try:
        records = (
            session.query(RouteRequest)
            .order_by(RouteRequest.created_at.desc())
            .limit(20)
            .all()
        )
        return jsonify([r.to_dict() for r in records])
    finally:
        session.close()


def _is_valid_coord(value):
    return (
        isinstance(value, (list, tuple))
        and len(value) == 2
        and all(isinstance(v, (int, float)) and not isinstance(v, bool) for v in value)
    )
