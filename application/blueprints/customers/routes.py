from math import ceil
from flask import request, jsonify
from sqlalchemy import select
from werkzeug.security import generate_password_hash, check_password_hash
from marshmallow import ValidationError

from application.extensions import db, limiter, cache
from application.models import Customer, ServiceTicket
from application.auth import encode_token
from . import customers_bp
from .schemas import customer_schema, customer_public, customers_public, login_schema


# =============================================================
# POST /customers/  → Create Customer
# =============================================================
@customers_bp.post("/")
@limiter.limit("20/minute")
def create_customer():
    try:
        data = customer_schema.load(request.json)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    exists = db.session.execute(
        select(Customer).where(Customer.email == data.email)
    ).scalars().first()

    if exists:
        return jsonify({"error": "Email already exists"}), 400

    data.password_hash = generate_password_hash(
        request.json["password"], method="pbkdf2:sha256"
    )

    db.session.add(data)
    db.session.commit()

    return customer_public.jsonify(data), 201


# =============================================================
# GET /customers/  → List
# =============================================================
@customers_bp.get("/")
@cache.cached(timeout=60, query_string=True)
def get_customers():
    page = max(int(request.args.get("page", 1)), 1)
    per_page = min(max(int(request.args.get("per_page", 10)), 1), 100)

    stmt = select(Customer).order_by(Customer.id.asc())
    total = db.session.execute(select(db.func.count()).select_from(Customer)).scalar() or 0

    customers = db.session.execute(
        stmt.limit(per_page).offset((page - 1) * per_page)
    ).scalars().all()

    return jsonify({
        "page": page,
        "per_page": per_page,
        "total": total,
        "pages": ceil(total / per_page),
        "items": customers_public.dump(customers)
    }), 200


# =============================================================
# GET /customers/<id>
# =============================================================
@customers_bp.get("/<int:customer_id>")
def get_customer(customer_id: int):
    cust = db.session.get(Customer, customer_id)
    if not cust:
        return jsonify({"error": "Customer not found"}), 404
    return customer_public.jsonify(cust), 200


# =============================================================
# PUT /customers/<id>
# =============================================================
@customers_bp.put("/<int:customer_id>")
def update_customer(customer_id: int):
    cust = db.session.get(Customer, customer_id)
    if not cust:
        return jsonify({"error": "Customer not found"}), 404

    payload = request.json or {}

    if "password" in payload:
        cust.password_hash = generate_password_hash(payload.pop("password"))

    for key in ("name", "email", "phone"):
        if key in payload:
            setattr(cust, key, payload[key])

    db.session.commit()
    cache.delete_memoized(get_customers)
    return customer_public.jsonify(cust), 200


# =============================================================
# DELETE /customers/<id>
# =============================================================
@customers_bp.delete("/<int:customer_id>")
def delete_customer(customer_id: int):
    cust = db.session.get(Customer, customer_id)
    if not cust:
        return jsonify({"error": "Customer not found"}), 404

    db.session.delete(cust)
    db.session.commit()
    cache.delete_memoized(get_customers)

    return jsonify({"message": "Customer deleted"}), 200


# =============================================================
# POST /customers/login/
# =============================================================
@customers_bp.post("/login/")
def login():
    try:
        data = login_schema.load(request.json)
    except ValidationError as err:
        return {"errors": err.messages}, 400

    cust = db.session.execute(
        select(Customer).where(Customer.email == data["email"])
    ).scalars().first()

    if not cust or not check_password_hash(cust.password_hash, data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401

    token = encode_token(cust.id)
    return jsonify({"token": token}), 200


# =============================================================
# GET /customers/my-tickets/
# =============================================================
@customers_bp.get("/my-tickets/")
def my_tickets():
    tickets = db.session.execute(
        select(ServiceTicket).order_by(ServiceTicket.id.asc())
    ).scalars().all()

    items = [{
        "ticket_id": t.id,
        "VIN": t.VIN,
        "service_date": t.service_date.isoformat(),
        "service_desc": t.service_desc
    } for t in tickets]

    return jsonify(items), 200
