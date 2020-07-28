# THIS FILE IS A SCRIPT THAT WILL CREATE THE TABLES IN OUR DATABASE

from sqlalchemy.orm import relationship
from sqlalchemy import create_engine, Column, Integer, ForeignKey, String, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash

Base = declarative_base()

# engine, suppose it has two tables 'user' and 'address' set up
engine = create_engine("mysql+pymysql://root:admin@localhost:3306/oc_p5")


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(150), unique=True)
    password_hash = Column(String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), unique=True)
    parent_id = Column(Integer, ForeignKey("category.id"))

    parent = relationship("Category", foreign_keys="Category.parent_id")


class Product(Base):
    __tablename__ = 'product'

    id = Column(BigInteger, primary_key=True)
    ref_id = Column(BigInteger, unique=True)
    name = Column(String(150))
    brand = Column(String(150))
    category_id = Column(Integer, ForeignKey("category.id"))
    description = Column(String(300))
    nutriscore = Column(Float)
    retailer = Column(String(150))
    url = Column(String(500))

    category = relationship("Category", foreign_keys="Product.category_id")


class Saved_Product(Base):
    __tablename__ = 'saved_product'

    id = Column(Integer, primary_key=True)
    original_product_id = Column(BigInteger, ForeignKey("product.id"))
    substitute_product_id = Column(BigInteger, ForeignKey("product.id"))
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User", foreign_keys="Saved_Product.user_id")
    original_product = relationship("Product", foreign_keys="Saved_Product.original_product_id")
    substitute_product = relationship("Product", foreign_keys="Saved_Product.substitute_product_id")


Base.metadata.create_all(engine)
