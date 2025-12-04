from marshmallow import fields, validate
from application.extensions import ma, db
from application.models import ServiceTicket, Mechanic, Inventory

# Public mechanic serializer
class MechanicPublicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Mechanic
        load_instance = True
        sqla_session = db.session

    id = fields.Int()
    name = fields.Str()


# Public part serializer
class PartPublicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Inventory
        load_instance = True
        sqla_session = db.session

    id = fields.Int()
    name = fields.Str()
    price = fields.Float()


# Main ticket schema
class ServiceTicketSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        sqla_session = db.session

    # TESTS REQUIRE BOTH NAMES TO WORK
    id = fields.Int(dump_only=True)
    ticket_id = fields.Int(attribute="id", dump_only=True)

    VIN = fields.Str(required=True)
    service_date = fields.Date(required=True)
    service_desc = fields.Str(required=True)
    customer_id = fields.Int(required=True)

    mechanics = fields.Nested(MechanicPublicSchema, many=True, dump_only=True)
    parts = fields.Nested(PartPublicSchema, many=True, dump_only=True)


ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)
