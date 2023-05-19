from src.db import db as database

Admin = database.get_collection('admins')
Product = database.get_collection('products')
ExploitationItem = database.get_collection('items')
Exploitation = database.get_collection('exploitations')