from os import environ

import dotenv

dotenv.load_dotenv()

TOKEN = environ['TOKEN']

TIME_OUT = 1000 * 60 * 60 * 24 * 7


ADMIN_ID = environ['ADMIN_1_ID']

ADMIN_IDS = [
    environ['ADMIN_1_ID']
]

MONGO_DB_URL = environ['MONGO_DB_URL']
