from application.extensions import ma, db
from application.models import Mechanic

class MechanicSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Mechanic
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field()
    name = ma.auto_field()
    email = ma.auto_field()
    phone = ma.auto_field()
    salary = ma.auto_field()

mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
