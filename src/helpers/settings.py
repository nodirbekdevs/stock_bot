from os import environ

import dotenv

dotenv.load_dotenv()

TOKEN = environ['STOCK_TOKEN']

TIME_OUT = 1000 * 60 * 60 * 24 * 7


ADMIN_ID = int(environ['STOCK_ADMIN_1_CHAT__ID'])

ADMINS = [773873885, 254396082]

MONGO_DB_URL = environ['STOCK_MONGO_DB_URL']
