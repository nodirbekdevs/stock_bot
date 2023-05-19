from aiogram import Dispatcher

# from src.handlers.exploitation import back_from_exploitation_handler
from src.handlers.utils import back_to_main_handler, paginate_handler

from src.states.admin import AdminStates
from src.states.exploitation import ExploitationStates
from src.states.product import ProductStates


def register_same_handlers(dp: Dispatcher):
    dp.register_callback_query_handler(back_to_main_handler, lambda query: query.data == "back",
                                       state=AdminStates.process)
    dp.register_callback_query_handler(back_to_main_handler, lambda query: query.data == "back",
                                       state=ExploitationStates.process)
    dp.register_callback_query_handler(back_to_main_handler, lambda query: query.data == "back",
                                       state=ProductStates.process)
    dp.register_callback_query_handler(paginate_handler, lambda query: query.data == "none", state="*")
