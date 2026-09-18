from flask import Blueprint, jsonify, request

from models import RouteRequest, SessionLocal
from routing import get_route

api_bp = Blueprint("api", __name__)


@api_bp.get("/health")
def health():
    return jsonify({"status": "ok"})


@api_bp.post("/route")
def create_route():
    payload = request.get_json(force=True)
    start = payload["start"]
    end = payload["end"]

    route = get_route(start, end)

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
