from application.extensions import ma, db
from application.models import Mechanic

class MechanicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Mechanic
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    email = ma.auto_field(required=True)
    phone = ma.auto_field(required=True)
    salary = ma.auto_field(required=True)

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
