class Config:
    SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:A4%40mysql@localhost/mechanic_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JSON_SORT_KEYS = False

class TestingConfig:
    pass

class ProductionConfig:
    pass
