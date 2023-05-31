from motor.motor_asyncio import AsyncIOMotorClient
from src.helpers.settings import MONGO_DB_URL

db_connection = AsyncIOMotorClient(MONGO_DB_URL)
db = db_connection['uztelecom_stock_project']


# from sqlalchemy import create_engine
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
#
# from src.helpers.settings import DB_URL
#
# Session = sessionmaker()
#
# engine = create_engine(DB_URL)
#
# Session.configure(bind=engine)
#
# session = Session()
#
# Base = declarative_base()


if __name__ == '__main__':
    pass
