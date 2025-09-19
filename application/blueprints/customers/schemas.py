from application.extensions import ma, db
from application.models import Customer
from marshmallow import fields

class CustomerSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Customer
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    phone = ma.auto_field()


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
