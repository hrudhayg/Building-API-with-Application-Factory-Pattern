from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from application.extensions import db
from application.models import Mechanic
from . import mechanics_bp
from .schemas import mechanic_schema, mechanics_schema


# POST '/' : Create
@mechanics_bp.post("/")
def create_mechanic():
    """
    Sample JSON body for Postman:
    {
        "name": "John Doe",
        "email": "johndoe@example.com",
        "phone": "123-456-7890",
        "salary": 55000.0
    }
    """
    try:
        mech = mechanic_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    exists = db.session.execute(
        select(Mechanic).where(Mechanic.email == mech.email)
    ).scalars().first()
    if exists:
        return jsonify({"error": "Mechanic email already exists"}), 400

    db.session.add(mech)
    db.session.commit()
    return mechanic_schema.jsonify(mech), 201


# GET '/' : Read all
@mechanics_bp.get("/")
def get_mechanics():
    mechs = db.session.execute(select(Mechanic)).scalars().all()
    return mechanics_schema.jsonify(mechs), 200


# GET '/<int:mechanic_id>' : Read one
@mechanics_bp.get("/<int:mechanic_id>")
def get_mechanic(mechanic_id: int):
    mech = db.session.get(Mechanic, mechanic_id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404
    return mechanic_schema.jsonify(mech), 200


# PUT '/<int:mechanic_id>' : Update
@mechanics_bp.put("/<int:mechanic_id>")
def update_mechanic(mechanic_id: int):
    mech = db.session.get(Mechanic, mechanic_id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404

    try:
        updated = mechanic_schema.load(request.json, instance=mech, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    db.session.commit()
    return mechanic_schema.jsonify(updated), 200


# DELETE '/<int:mechanic_id>' : Delete
@mechanics_bp.delete("/<int:mechanic_id>")
def delete_mechanic(mechanic_id: int):
    mech = db.session.get(Mechanic, mechanic_id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404

    # If there's a many-to-many with tickets, clear junction rows first
    if hasattr(mech, "tickets"):
        mech.tickets.clear()

    db.session.delete(mech)
    db.session.commit()
    return jsonify({"message": "Mechanic deleted"}), 200
