from marshmallow import fields
from application.extensions import ma, db
from application.models import ServiceTicket, Mechanic, Inventory

class MechanicPublicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Mechanic
        load_instance = True
        sqla_session = db.session

    mechanic_id = fields.Integer(attribute="id", dump_only=True)
    name = ma.auto_field()

class PartPublicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inventory
        load_instance = True
        sqla_session = db.session

    part_id = fields.Integer(attribute="id", dump_only=True)
    name = ma.auto_field()
    price = ma.auto_field()

class ServiceTicketSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        sqla_session = db.session

    ticket_id = fields.Integer(attribute="id", dump_only=True)
    VIN = ma.auto_field(required=True)
    service_date = ma.auto_field(required=True)  # YYYY-MM-DD
    service_desc = ma.auto_field(required=True)
    customer_id = ma.auto_field(required=True)

    mechanics = ma.Nested(MechanicPublicSchema, many=True, dump_only=True)
    parts = ma.Nested(PartPublicSchema, many=True, dump_only=True)

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)
