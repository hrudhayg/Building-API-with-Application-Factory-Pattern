from flask import request, jsonify
from sqlalchemy import select, func

from application.extensions import db, limiter
from application.models import Mechanic, ServiceTicket, service_mechanics
from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema   # <-- only mechanic schemas

# POST '/'
@mechanics_bp.post("/")
@limiter.limit("20/minute")
def create_mechanic():
    data = mechanic_schema.load(request.json)
    exists = db.session.execute(
        select(Mechanic).where(Mechanic.email == data.email)
    ).scalars().first()
    if exists:
        return jsonify({"error": "Mechanic email already exists"}), 400
    db.session.add(data)
    db.session.commit()
    return mechanic_schema.jsonify(data), 201

# GET '/'
@mechanics_bp.get("/")
def get_mechanics():
    mechs = db.session.execute(
        select(Mechanic).order_by(Mechanic.id.asc())
    ).scalars().all()
    return mechanics_schema.jsonify(mechs), 200

# GET '/<id>'
@mechanics_bp.get("/<int:mechanic_id>")
def get_mechanic(mechanic_id: int):
    mech = db.session.get(Mechanic, mechanic_id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404
    return mechanic_schema.jsonify(mech), 200

# PUT '/<id>'
@mechanics_bp.put("/<int:mechanic_id>")
def update_mechanic(mechanic_id: int):
    mech = db.session.get(Mechanic, mechanic_id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404
    payload = request.json or {}
    for key in ("name", "email", "phone", "salary"):
        if key in payload:
            setattr(mech, key, payload[key])
    db.session.commit()
    return mechanic_schema.jsonify(mech), 200

# DELETE '/<id>'
@mechanics_bp.delete("/<int:mechanic_id>")
def delete_mechanic(mechanic_id: int):
    mech = db.session.get(Mechanic, mechanic_id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404
    mech.tickets.clear()
    db.session.delete(mech)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted"}), 200

# GET '/leaderboard'
@mechanics_bp.get("/leaderboard")
def leaderboard():
    rows = db.session.execute(
        select(
            Mechanic.id,
            Mechanic.name,
            func.count(service_mechanics.c.ticket_id).label("ticket_count")
        )
        .join(service_mechanics, Mechanic.id == service_mechanics.c.mechanic_id, isouter=True)
        .group_by(Mechanic.id, Mechanic.name)
        .order_by(func.count(service_mechanics.c.ticket_id).desc(), Mechanic.id.asc())
    ).all()
    return jsonify([
        {"mechanic_id": r.id, "name": r.name, "ticket_count": int(r.ticket_count)}
        for r in rows
    ]), 200
