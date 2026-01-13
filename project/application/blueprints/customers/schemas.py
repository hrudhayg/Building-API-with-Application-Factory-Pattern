from marshmallow import fields, validate
from ...extensions import ma, db
from ...models import Customer

class CustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
        load_instance = True
        sqla_session = db.session

    # EXPLICIT FIELDS
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1))
    email = fields.Email(required=True)
    phone = fields.Str(required=True)

    # This is NOT a DB field → only input
    password = fields.Str(required=True, load_only=True)

    # MUST NOT be required when creating
    password_hash = fields.Str(dump_only=True)


class CustomerPublicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
        load_instance = True
        sqla_session = db.session

    id = fields.Int()
    name = fields.Str()
    email = fields.Email()
    phone = fields.Str()


class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)


customer_schema = CustomerSchema()
customer_public = CustomerPublicSchema()
customers_public = CustomerPublicSchema(many=True)
login_schema = LoginSchema()
