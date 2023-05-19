from mongoengine import Document, StringField, IntField, DateTimeField
from datetime import datetime


class MongoProduct(Document):
    admin_id = IntField(unique=True, required=True)
    name = StringField(max_length=255, default='')
    count = IntField(default=0)
    in_use = IntField(default=0)
    not_in_use = IntField(default=0)
    status = StringField(choices=['process', 'inactive', 'active'], default='process')
    updated_at = DateTimeField(default=datetime.utcnow)
    created_at = DateTimeField(default=datetime.now)


# from sqlalchemy import Column, String, Integer
# from src.db import Base, session
#
#
# class Product(Base):
#     __tablename__ = "prodcuts"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     name = Column(String, default="")
#     count = Column(Integer, default=0)
#     in_use = Column(Integer, default=0)
#     not_in_use = Column(Integer, default=0)
#
#     def __init__(self, product):
#         self.product_id = product.product_id
#         self.name = product.name
#         self.count = product.count
#         self.in_use = product.in_use if product.in_use else 0
#         self.not_in_use = product.not_in_use if product.not_in_use else 0
#
#     def add_commit(self):
#         session.add(self)
#         session.commit()
#
#     def update_commit(self):
#         session.commit()
#
#     def __repr__(self):
#         return "<Product (product_id='%i', product_name='%s', username='%s')>" % (
#             self.user_id, self.first_name, self.username
#         )
