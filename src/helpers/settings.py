from os import environ

import dotenv

dotenv.load_dotenv()

TOKEN = environ['TOKEN']

# Database info
# DB_DIALECT = "postgresql"
# DB_HOSTNAME = environ['DATABASE_HOST']
# DB_USERNAME = environ['DATABASE_USER']
# DB_PASSWORD = environ['DATABASE_PASSWORD']
# DB_DATABASE = environ['DATABASE_NAME']

ADMIN_IDS = [
    environ['ADMIN_1_ID']
]

# DB_URL = "%s://%s:%s@%s/%s" % (
#     DB_DIALECT,
#     DB_USERNAME,
#     DB_PASSWORD,
#     DB_HOSTNAME,
#     DB_DATABASE
# )

# DB_URL = f"{DB_DIALECT}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOSTNAME}/{DB_DATABASE}"

MONGO_DB_URL = environ['MONGO_DB_URL']
