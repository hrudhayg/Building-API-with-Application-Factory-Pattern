from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError

from project.application.extensions import db, limiter
from project.application.models import Inventory
from . import inventory_bp
from .schemas import inventory_schema, inventories_schema


# ============================================================
# CREATE PART → POST /inventory and /inventory/
# ============================================================
@inventory_bp.post("")
@inventory_bp.post("/")
@limiter.limit("30/minute")
def create_part():
    try:
        part = inventory_schema.load(request.json)
    except ValidationError as err:
        return jsonify({"errors": err.messages}), 400

    db.session.add(part)
    db.session.commit()
    return inventory_schema.jsonify(part), 201


# ============================================================
# LIST PARTS → GET /inventory and /inventory/
# ============================================================
@inventory_bp.get("")
@inventory_bp.get("/")
def get_parts():
    parts = db.session.execute(
        select(Inventory).order_by(Inventory.id.asc())
    ).scalars().all()
    return inventories_schema.jsonify(parts), 200


# ============================================================
# GET SINGLE PART → GET /inventory/<id>
# ============================================================
@inventory_bp.get("<int:part_id>")
def get_part(part_id: int):
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404
    return inventory_schema.jsonify(part), 200


# ============================================================
# UPDATE PART → PUT /inventory/<id>
# ============================================================
@inventory_bp.put("<int:part_id>")
def update_part(part_id: int):
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404

    payload = request.json or {}
    if "name" in payload:
        part.name = payload["name"]
    if "price" in payload:
        part.price = payload["price"]

    db.session.commit()
    return inventory_schema.jsonify(part), 200


# ============================================================
# DELETE PART → DELETE /inventory/<id>
# ============================================================
@inventory_bp.delete("<int:part_id>")
def delete_part(part_id: int):
    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404

    db.session.delete(part)
    db.session.commit()
    return jsonify({"message": "Part deleted"}), 200
