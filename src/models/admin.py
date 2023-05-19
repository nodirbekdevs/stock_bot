from mongoengine import Document, StringField, IntField, DateTimeField, BooleanField
from datetime import datetime


class MongoAdmin(Document):
    admin_id = IntField(unique=True, required=True)
    first_name = StringField(max_length=255, default='')
    last_name = StringField(max_length=255, default='')
    username = StringField(max_length=255, default='')
    is_using = BooleanField(default=False)
    status = StringField(choices=['process', 'inactive', 'active'], default='process')
    created_at = DateTimeField(default=datetime.now)


# from sqlalchemy import Column, String, BIGINT, Integer
# from src.db import Base, session
#
#
# class Admin(Base):
#     __tablename__ = "admins"
#
#     id = Column(Integer, primary_key=True, autoincrement=True)
#     admin_id = Column(BIGINT, primary_key=True)
#     first_name = Column(String, nullable=False)
#     last_name = Column(String)
#     username = Column(String)
#
#     def __init__(self, admin):
#         self.admin_id = admin.id
#         self.first_name = admin.first_name
#         self.last_name = admin.last_name
#         self.username = admin.username
#
#     def commit(self):
#         session.add(self)
#         session.commit()
#
#     def __repr__(self):
#         return "<Admin (admin_id='%i', first_name='%s', username='%s')>" % (
#             self.user_id, self.first_name, self.username
#     )