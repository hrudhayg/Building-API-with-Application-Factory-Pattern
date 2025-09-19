from marshmallow import fields
from application.extensions import ma, db
from application.models import ServiceTicket, Mechanic

class MechanicPublicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Mechanic
        load_instance = True
        sqla_session = db.session

    # expose mechanic_id and name only (clean API surface)
    mechanic_id = fields.Integer(attribute="id", dump_only=True)
    name = ma.auto_field()

class ServiceTicketSchema(ma.SQLAlchemySchema):
    class Meta:
        model = ServiceTicket
        load_instance = True
        sqla_session = db.session

    # alias "id" -> "ticket_id" in output
    ticket_id = fields.Integer(attribute="id", dump_only=True)

    VIN = ma.auto_field()
    service_date = ma.auto_field()         # YYYY-MM-DD
    service_desc = ma.auto_field()
    customer_id = ma.auto_field()

    # mechanics list with mechanic_id + name
    mechanics = ma.Nested(MechanicPublicSchema, many=True, dump_only=True)

ticket_schema = ServiceTicketSchema()
tickets_schema = ServiceTicketSchema(many=True)
