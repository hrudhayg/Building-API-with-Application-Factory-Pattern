from typing import List
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Date, Float, ForeignKey
from .extensions import db

# ---- Association Tables ----
service_mechanics = db.Table(
    "service_mechanics",
    db.metadata,
    db.Column("ticket_id", ForeignKey("service_tickets.id"), primary_key=True),
    db.Column("mechanic_id", ForeignKey("mechanics.id"), primary_key=True),
)

service_ticket_parts = db.Table(
    "service_ticket_parts",
    db.metadata,
    db.Column("ticket_id", ForeignKey("service_tickets.id"), primary_key=True),
    db.Column("inventory_id", ForeignKey("inventory.id"), primary_key=True),
)

# ---- Models ----
class Customer(db.Model):
    __tablename__ = "customers"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)

    tickets: Mapped[List["ServiceTicket"]] = db.relationship(
        back_populates="customer", cascade="all, delete-orphan"
    )

class Mechanic(db.Model):
    __tablename__ = "mechanics"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=False)
    salary: Mapped[float] = mapped_column(Float, nullable=False)

    tickets: Mapped[List["ServiceTicket"]] = db.relationship(
        secondary=service_mechanics, back_populates="mechanics"
    )

class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"
    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(String(100), nullable=False)
    service_date: Mapped[datetime.date] = mapped_column(Date, nullable=False)
    service_desc: Mapped[str] = mapped_column(String(255), nullable=False)

    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))
    customer: Mapped["Customer"] = db.relationship(back_populates="tickets")

    mechanics: Mapped[List["Mechanic"]] = db.relationship(
        secondary=service_mechanics, back_populates="tickets"
    )

    parts: Mapped[List["Inventory"]] = db.relationship(
        secondary=service_ticket_parts, back_populates="tickets"
    )

class Inventory(db.Model):
    __tablename__ = "inventory"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    price: Mapped[float] = mapped_column(Float, nullable=False)

    tickets: Mapped[List["ServiceTicket"]] = db.relationship(
        secondary=service_ticket_parts, back_populates="parts"
    )
