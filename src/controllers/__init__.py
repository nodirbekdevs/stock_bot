from src.controllers.admin import Admin, AdminController
from src.controllers.product import Product, ProductController
from src.controllers.exploitation import Exploitation, ExploitationController
from src.controllers.exploitation_items import ExploitationItem, ExploitationItemsController

admin_controller = AdminController(Admin)
product_controller = ProductController(Product)
exploitation_controller = ExploitationController(Exploitation)
exploitation_items_controller = ExploitationItemsController(ExploitationItem)
