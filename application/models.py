from datetime import date
from typing import List
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey
from .extensions import db

# Association (Many-to-Many) between ServiceTicket and Mechanic
service_mechanics = db.Table(
    "service_mechanics",
    db.metadata,
    db.Column("ticket_id", ForeignKey("service_tickets.id"), primary_key=True),
    db.Column("mechanic_id", ForeignKey("mechanics.id"), primary_key=True),
)

class Customer(db.Model):
    __tablename__ = "customers"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)

    # One-to-many: customer -> tickets
    tickets: Mapped[List["ServiceTicket"]] = db.relationship(back_populates="customer")

class ServiceTicket(db.Model):
    __tablename__ = "service_tickets"

    id: Mapped[int] = mapped_column(primary_key=True)
    VIN: Mapped[str] = mapped_column(db.String(100), nullable=False)
    service_date: Mapped[date] = mapped_column(db.Date, nullable=False)
    service_desc: Mapped[str] = mapped_column(db.String(255), nullable=False)
    customer_id: Mapped[int] = mapped_column(ForeignKey("customers.id"))

    customer: Mapped["Customer"] = db.relationship(back_populates="tickets")

    # Many-to-many with mechanics
    mechanics: Mapped[List["Mechanic"]] = db.relationship(
        secondary=service_mechanics,
        back_populates="tickets",
    )

class Mechanic(db.Model):
    __tablename__ = "mechanics"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(255), nullable=False, unique=True)
    phone: Mapped[str] = mapped_column(db.String(20), nullable=False)
    salary: Mapped[float] = mapped_column(db.Float, nullable=False)

    tickets: Mapped[List["ServiceTicket"]] = db.relationship(
        secondary=service_mechanics,
        back_populates="mechanics",
    )
