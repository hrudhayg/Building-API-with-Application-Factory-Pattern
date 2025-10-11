from flask import request, jsonify
from sqlalchemy import select
from application.extensions import db, limiter
from application.models import Inventory
from . import inventory_bp
from .schemas import inventory_schema, inventories_schema

@inventory_bp.post("/")
@limiter.limit("30/minute")
def create_part():
    part = inventory_schema.load(request.json)
    db.session.add(part)
    db.session.commit()
    return inventory_schema.jsonify(part), 201

@inventory_bp.get("/")
def list_parts():
    parts = db.session.execute(
        select(Inventory).order_by(Inventory.id.asc())
    ).scalars().all()
    return inventories_schema.jsonify(parts), 200

@inventory_bp.get("/<int:part_id>")
def get_part(part_id: int):
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404
    return inventory_schema.jsonify(part), 200

@inventory_bp.put("/<int:part_id>")
def update_part(part_id: int):
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404
    payload = request.json or {}
    for k in ("name", "price"):
        if k in payload:
            setattr(part, k, payload[k])
    db.session.commit()
    return inventory_schema.jsonify(part), 200

@inventory_bp.delete("/<int:part_id>")
def delete_part(part_id: int):
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404
    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": "Part deleted"}), 200
