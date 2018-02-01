from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Base, Category, Product

engine = create_engine('sqlite:///trialDatabaseUsersCart.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
# A DBSession() instance establishes all conversations with the database
# and represents a "staging zone" for all the objects loaded into the
# database session object. Any change made against the objects in the
# session won't be persisted into the database until you call
# session.commit(). If you're not happy about the changes, you can
# revert all of them back to the last commit by calling
# session.rollback()
session = DBSession()


# Dummy Categories
category1 = Category(name="Fashion", description="Clothing, shoes, and other")

session.add(category1)
session.commit()

category2 = Category(name="Entertainment", description="TV, Games, and other")

session.add(category2)
session.commit()

category3 = Category(name="Stationary", description="Books")

session.add(category3)
session.commit()

# Dummy Products
product1 = Product(name="Batakali", description="Shirt", price="5.23", 
			category=category1)

session.add(product1)
session.commit()

product2 = Product(name="Techno Tv", description="Television Set", 
			price="12.45", category=category2)

session.add(product2)
session.commit()

product3 = Product(name="Code Book", description="Algorithms Book",
			price="65.45", category=category3)

session.add(product3)
session.commit()



print("Sample test data add!")