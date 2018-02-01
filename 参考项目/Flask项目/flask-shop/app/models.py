# Import the database object (db) from the main application module
from app import db

# Define a base model for other database tables to inherit
class Base(db.Model):

    __abstract__  = True

    id            = db.Column(db.Integer, primary_key=True)
    date_created  = db.Column(db.DateTime,  default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime,  default=db.func.current_timestamp(),
                                           onupdate=db.func.current_timestamp())

# Define a Stock model
class Stock(Base):

    __tablename__ = 'stock_av'

    # product Name
    name    = db.Column(db.String(128),  nullable=False, unique=True )

    # Product data: price & quantity
    price     = db.Column(db.Integer, nullable=False)
    quantity   = db.Column(db.Integer, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, price, quantity):

        self.name     = name
        self.price    = price
        self.quantity = quantity

# Define a purchase model
class Purchase(Base):

    __tablename__ = 'purchase_report'

    # product Name
    name    = db.Column(db.String(128),  nullable=False)

    # Product quantity
    quantity   = db.Column(db.Integer, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, quantity):

        self.name     = name
        self.quantity = quantity
# Define a Sell model
class Sell(Base):

    __tablename__ = 'sell_report'

    # product Name
    name    = db.Column(db.String(128),  nullable=False)

    # Product quantity
    quantity   = db.Column(db.Integer, nullable=False)

    # New instance instantiation procedure
    def __init__(self, name, quantity):

        self.name     = name
        self.quantity = quantity
