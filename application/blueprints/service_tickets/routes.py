from functools import wraps
from flask import request, jsonify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from application.extensions import db, limiter, cache
from application.models import ServiceTicket, Mechanic, Customer, Inventory
from application.auth import token_required
from . import service_tickets_bp
from .schemas import ticket_schema, tickets_schema

def _verify_customer(customer_id: int) -> bool:
    return db.session.get(Customer, customer_id) is not None

# POST '/' : Create ticket
@service_tickets_bp.post("/")
@limiter.limit("15/minute")
def create_ticket():
    """
    {
      "VIN": "1HGCM82633A004352",
      "service_date": "2025-09-01",
      "service_desc": "Oil + brakes",
      "customer_id": 1,
      "mechanic_ids": [1,2]     // optional
    }
    """
    payload = request.json or {}
    mechanic_ids = payload.pop("mechanic_ids", [])
    try:
        ticket = ticket_schema.load(payload)
    except Exception as e:
        return jsonify(getattr(e, "messages", {"error": "Invalid data"})), 400

    if not _verify_customer(ticket.customer_id):
        return jsonify({"error": f"customer_id {ticket.customer_id} not found"}), 400

    if mechanic_ids:
        mechs = db.session.execute(select(Mechanic).where(Mechanic.id.in_(mechanic_ids))).scalars().all()
        if len(mechs) != len(set(mechanic_ids)):
            return jsonify({"error": "One or more mechanic_ids not found"}), 400
        ticket.mechanics = mechs

    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Foreign key error (customer/mechanic)."}), 400

    cache.delete_memoized(get_tickets)
    return ticket_schema.jsonify(ticket), 201

# GET '/' : List all (cached)
@service_tickets_bp.get("/")
@cache.cached(timeout=60)
def get_tickets():
    tickets = db.session.execute(select(ServiceTicket).order_by(ServiceTicket.id.asc())).scalars().all()
    return tickets_schema.jsonify(tickets), 200

# GET '/<id>'
@service_tickets_bp.get("/<int:ticket_id>")
def get_ticket(ticket_id: int):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    return ticket_schema.jsonify(ticket), 200

# PUT '/<id>' : Update fields; mechanics via mechanic_ids replaces list
@service_tickets_bp.put("/<int:ticket_id>")
@token_required
def update_ticket(ticket_id: int, customer_id: int):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    if ticket.customer_id != customer_id:
        return jsonify({"error": "Forbidden"}), 403

    payload = request.json or {}
    mechanic_ids = payload.pop("mechanic_ids", None)

    try:
        updated = ticket_schema.load(payload, instance=ticket, partial=True)
    except Exception as e:
        return jsonify(getattr(e, "messages", {"error": "Invalid data"})), 400

    if "customer_id" in payload and not _verify_customer(updated.customer_id):
        return jsonify({"error": f"customer_id {updated.customer_id} not found"}), 400

    if mechanic_ids is not None:
        mechs = db.session.execute(select(Mechanic).where(Mechanic.id.in_(mechanic_ids))).scalars().all()
        if len(mechs) != len(set(mechanic_ids)):
            return jsonify({"error": "One or more mechanic_ids not found"}), 400
        updated.mechanics = mechs

    db.session.commit()
    cache.delete_memoized(get_tickets)
    return ticket_schema.jsonify(updated), 200

# DELETE '/<id>'
@service_tickets_bp.delete("/<int:ticket_id>")
@token_required
def delete_ticket(ticket_id: int, customer_id: int):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    if ticket.customer_id != customer_id:
        return jsonify({"error": "Forbidden"}), 403

    ticket.mechanics.clear()
    ticket.parts.clear()
    db.session.delete(ticket)
    db.session.commit()
    cache.delete_memoized(get_tickets)
    return jsonify({"message": "Ticket deleted"}), 200

# PUT '/<ticket_id>/edit' : add/remove mechanics
@service_tickets_bp.put("/<int:ticket_id>/edit")
@token_required
def edit_mechanics(ticket_id: int, customer_id: int):
    """
    {
      "add_ids": [2,3],
      "remove_ids": [1]
    }
    """
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    if ticket.customer_id != customer_id:
        return jsonify({"error": "Forbidden"}), 403

    payload = request.json or {}
    add_ids = payload.get("add_ids", []) or []
    remove_ids = payload.get("remove_ids", []) or []

    for mid in add_ids:
        mech = db.session.get(Mechanic, int(mid))
        if not mech:
            return jsonify({"error": f"Mechanic {mid} not found"}), 404
        if mech not in ticket.mechanics:
            ticket.mechanics.append(mech)

    for mid in remove_ids:
        mech = db.session.get(Mechanic, int(mid))
        if not mech:
            return jsonify({"error": f"Mechanic {mid} not found"}), 404
        if mech in ticket.mechanics:
            ticket.mechanics.remove(mech)

    db.session.commit()
    return ticket_schema.jsonify(ticket), 200

# POST '/<ticket_id>/add-part/<part_id>' : add inventory item to ticket
@service_tickets_bp.post("/<int:ticket_id>/add-part/<int:part_id>")
@token_required
def add_part(ticket_id: int, part_id: int, customer_id: int):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    if ticket.customer_id != customer_id:
        return jsonify({"error": "Forbidden"}), 403

    part = db.session.get(Inventory, part_id)
    if not part:
        return jsonify({"error": "Part not found"}), 404

    if part not in ticket.parts:
        ticket.parts.append(part)
        db.session.commit()
    return ticket_schema.jsonify(ticket), 200
