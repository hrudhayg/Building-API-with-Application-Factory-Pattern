from marshmallow import fields, validate
from application.extensions import ma, db
from application.models import Customer

class CustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True, validate=validate.Length(min=1))
    email = ma.auto_field(required=True)
    phone = ma.auto_field(required=True)
    # Write-only password (not mapped column name; we hydrate to password_hash in route)
    password = fields.String(load_only=True, required=True)

class CustomerPublicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    phone = ma.auto_field()

# For login
class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)

customer_schema = CustomerSchema()
customer_public = CustomerPublicSchema()
customers_public = CustomerPublicSchema(many=True)
login_schema = LoginSchema()
