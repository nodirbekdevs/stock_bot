from typing import List
from src.models import Admin
from src.models.admin import MongoAdmin


class AdminController:
    def __init__(self, model: Admin):
        self.model = model

    async def get_all(self, query: dict) -> List[Admin]:
        try:
            length = await self.model.count_documents(query)
            return await self.model.find(query).to_list(length=length)
        except Exception as error:
            print(error)

    async def get_one(self, query: dict) -> Admin:
        try:
            return await self.model.find_one(query)
        except Exception as error:
            print(error)

    async def get_pagination(self, query: dict, offset: int, limit: int) -> List[Admin]:
        try:
            return await self.model.find(query).skip(offset).limit(limit).to_list(length=limit)
        except Exception as error:
            print(error)

    async def make(self, data: dict) -> Admin:
        try:
            model = MongoAdmin()

            for key, value in data.items():
                setattr(model, key, value)

            return await self.model.insert_one(model.to_mongo())
        except Exception as error:
            print(error)

    async def update(self, query: dict, data: dict):
        try:
            return await self.model.update_one(query, {"$set": data})
        except Exception as error:
            print(error)

    async def increment(self, query: dict, data: dict):
        try:
            return await self.model.update_one(query, {'$inc': data})
        except Exception as error:
            print(error)

    async def delete(self, query: dict):
        try:
            return await self.model.delete_one(query)
        except Exception as error:
            print(error)

    async def count(self, query: dict):
        try:
            return await self.model.count_documents(query)
        except Exception as error:
            print(error)


# from src.db import session

# class AdminController:
#     def __init__(self, model):
#         self.model = model
#
#     def get_all(self, query: dict) -> List[Admin]:
#         try:
#             return session.query(self.model).filter(**query).all()
#         except Exception as error:
#             print(error)
#
#     def get_one(self, query: dict) -> Admin:
#         try:
#             return session.query(self.model).filter(**query).first()
#         except Exception as error:
#             print(error)
#
#     def get_pagination(self, query: dict, offset: int, limit: int) -> List[Admin]:
#         try:
#             return session.query(self.model).filter(**query).offset(offset).limit(limit).all()
#         except Exception as error:
#             print(error)
#
#     @staticmethod
#     def make(data) -> Admin:
#         try:
#             admin = Admin(data)
#             admin.commit()
#
#             return admin
#         except Exception as error:
#             print(error)
#
#     def update(self, query: dict, data: dict):
#         try:
#             updated = session.query(self.model).filter_by(**query).update(data)
#             session.commit()
#             return updated
#         except Exception as error:
#             print(error)
#
#     def delete(self, query: dict):
#         try:
#             admin = session.query(self.model)
#
#             if query['admin_id']:
#                 admin = admin.filter_by(admin_id=query['admin_id']).first()
#             elif query['first_name']:
#                 admin = admin.filter_by(first_name=query['first_name']).first()
#             elif query['last_name']:
#                 admin = admin.filter_by(last_name=query['last_name']).first()
#             elif query['username']:
#                 admin = admin.filter_by(username=query['username']).first()
#
#             session.delete(admin)
#             session.commit()
#         except Exception as error:
#             print(error)