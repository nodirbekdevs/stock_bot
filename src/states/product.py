from aiogram.dispatcher.filters.state import StatesGroup, State


class ProductStates(StatesGroup):
    process = State()
    all_products = State()
    one_product = State()
    add = State()
    name = State()
    count = State()