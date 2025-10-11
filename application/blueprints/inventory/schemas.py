from application.extensions import ma, db
from application.models import Inventory

class InventorySchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Inventory
        load_instance = True
        sqla_session = db.session

    id = ma.auto_field(dump_only=True)
    name = ma.auto_field(required=True)
    price = ma.auto_field(required=True)

inventory_schema = InventorySchema()
inventories_schema = InventorySchema(many=True)
