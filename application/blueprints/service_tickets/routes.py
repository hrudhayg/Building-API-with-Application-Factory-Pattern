from flask import request, jsonify
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

from application.extensions import db
from application.models import ServiceTicket, Mechanic, Customer
from . import service_tickets_bp
from .schemas import ticket_schema, tickets_schema

# POST '/' : Create service ticket
# Postman sample:
# {
#   "VIN": "1HGCM82633A004352",
#   "service_date": "2025-09-01",
#   "service_desc": "Oil + brakes",
#   "customer_id": 1   // make sure this customer exists
# }
@service_tickets_bp.post("/")
def create_ticket():
    try:
        ticket = ticket_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # friendly FK check before hitting DB
    cust = db.session.get(Customer, ticket.customer_id)
    if not cust:
        return jsonify({"error": f"customer_id {ticket.customer_id} not found"}), 400

    db.session.add(ticket)
    try:
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Invalid foreign key. Ensure customer_id exists."}), 400

    return ticket_schema.jsonify(ticket), 201

# GET '/' : List all tickets
@service_tickets_bp.get("/")
def get_tickets():
    tickets = db.session.execute(select(ServiceTicket)).scalars().all()
    return tickets_schema.jsonify(tickets), 200

# GET '/<int:ticket_id>' : Read one
@service_tickets_bp.get("/<int:ticket_id>")
def get_ticket(ticket_id: int):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    return ticket_schema.jsonify(ticket), 200

# PUT '/<int:ticket_id>' : Update ticket fields (not relationships)
# Postman sample (any subset):
# {
#   "service_desc": "Oil + brakes + tire rotation",
#   "service_date": "2025-09-03"
# }
@service_tickets_bp.put("/<int:ticket_id>")
def update_ticket(ticket_id: int):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    try:
        updated = ticket_schema.load(request.json, instance=ticket, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400

    # if customer_id was changed, validate it
    if "customer_id" in (request.json or {}):
        cust = db.session.get(Customer, updated.customer_id)
        if not cust:
            return jsonify({"error": f"customer_id {updated.customer_id} not found"}), 400

    db.session.commit()
    return ticket_schema.jsonify(updated), 200

# DELETE '/<int:ticket_id>' : Delete
@service_tickets_bp.delete("/<int:ticket_id>")
def delete_ticket(ticket_id: int):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    # clear many-to-many junctions first
    if hasattr(ticket, "mechanics"):
        ticket.mechanics.clear()
    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Ticket deleted"}), 200

# PUT '/<ticket_id>/assign-mechanic/<mechanic_id>'
@service_tickets_bp.put("/<int:ticket_id>/assign-mechanic/<int:mechanic_id>")
def assign_mechanic(ticket_id: int, mechanic_id: int):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    mech = db.session.get(Mechanic, mechanic_id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404
    if mech not in ticket.mechanics:
        ticket.mechanics.append(mech)
        db.session.commit()
    return ticket_schema.jsonify(ticket), 200

# PUT '/<ticket_id>/remove-mechanic/<mechanic_id>'
@service_tickets_bp.put("/<int:ticket_id>/remove-mechanic/<int:mechanic_id>")
def remove_mechanic(ticket_id: int, mechanic_id: int):
    ticket = db.session.get(ServiceTicket, ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404
    mech = db.session.get(Mechanic, mechanic_id)
    if not mech:
        return jsonify({"error": "Mechanic not found"}), 404
    if mech in ticket.mechanics:
        ticket.mechanics.remove(mech)
        db.session.commit()
    return ticket_schema.jsonify(ticket), 200
