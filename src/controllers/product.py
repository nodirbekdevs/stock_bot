from typing import List
from src.models import Product
from src.models.product import MongoProduct


class ProductController:
    def __init__(self, model: Product):
        self.model = model

    async def get_all(self, query: dict) -> List[Product]:
        try:
            length = await self.model.count_documents(query)
            return await self.model.find(query).to_list(length=length)
        except Exception as error:
            print(error)

    async def get_one(self, query: dict) -> Product:
        try:
            return await self.model.find_one(query)
        except Exception as error:
            print(error)

    async def get_pagination(self, query: dict, offset: int, limit: int) -> List[Product]:
        try:
            return await self.model.find(query).skip(offset).limit(limit).to_list(length=limit)
        except Exception as error:
            print(error)

    async def make(self, data: dict) -> Product:
        try:
            model = MongoProduct()

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


# class ProductController:
#     def __init__(self, model):
#         self.model = model
#
#     def get_all(self, query: dict) -> List[Product]:
#         try:
#             return session.query(self.model).filter(**query).all()
#         except Exception as error:
#             print(error)
#
#     def get_one(self, query: dict) -> Product:
#         try:
#             return session.query(self.model).filter(**query).first()
#         except Exception as error:
#             print(error)
#
#     def get_pagination(self, query: dict, offset: int, limit: int) -> List[Product]:
#         try:
#             return session.query(self.model).filter(**query).offset(offset).limit(limit).all()
#         except Exception as error:
#             print(error)
#
#     @staticmethod
#     def make(data) -> Product:
#         try:
#             product = Product(data)
#
#             product.commit()
#
#             return product
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
#             product = session.query(self.model)
#
#             if query['id']:
#                 product = product.filter_by(id=query['id']).first()
#             elif query['name']:
#                 product = product.filter_by(name=query['name']).first()
#
#             session.delete(product)
#             session.commit()
#         except Exception as error:
#             print(error)