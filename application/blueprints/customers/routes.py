from flask import request, jsonify
from sqlalchemy import select
from marshmallow import ValidationError
from application.extensions import db
from application.models import Customer
from . import customers_bp
from .schemas import customer_schema, customers_schema

@customers_bp.post("/")
def create_customer():
    try:
        cust = customer_schema.load(request.json)
    except ValidationError as e:
        return jsonify(e.messages), 400
    exists = db.session.execute(
        select(Customer).where(Customer.email == cust.email)
    ).scalars().first()
    if exists:
        return jsonify({"error": "Email already exists"}), 400
    db.session.add(cust)
    db.session.commit()
    return customer_schema.jsonify(cust), 201

@customers_bp.get("/")
def get_customers():
    customers = db.session.execute(select(Customer)).scalars().all()
    return customers_schema.jsonify(customers), 200

@customers_bp.get("/<int:customer_id>")
def get_customer(customer_id: int):
    cust = db.session.get(Customer, customer_id)
    if not cust:
        return jsonify({"error": "Customer not found"}), 404
    return customer_schema.jsonify(cust), 200

@customers_bp.put("/<int:customer_id>")
def update_customer(customer_id: int):
    cust = db.session.get(Customer, customer_id)
    if not cust:
        return jsonify({"error": "Customer not found"}), 404
    try:
        updated = customer_schema.load(request.json, instance=cust, partial=True)
    except ValidationError as e:
        return jsonify(e.messages), 400
    db.session.commit()
    return customer_schema.jsonify(updated), 200

@customers_bp.delete("/<int:customer_id>")
def delete_customer(customer_id: int):
    cust = db.session.get(Customer, customer_id)
    if not cust:
        return jsonify({"error": "Customer not found"}), 404
    db.session.delete(cust)
    db.session.commit()
    return jsonify({"message": "Customer deleted"}), 200
