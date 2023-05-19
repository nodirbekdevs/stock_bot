from datetime import datetime

from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from src.loader import dp, bot
from src.models import Admin, Product, Exploitation, ExploitationItem
from src.controllers import admin_controller, product_controller, exploitation_controller, exploitation_items_controller
from src.helpers.keyboards import main_keyboard, exploitation_keyboard, back_keyboard, one_exploitation_product_keyboard, one_using_exploitation_keyboard
from src.helpers.utils import Pagination, is_num
from src.helpers.format import product_format, exploitation_format
from src.states.exploitation import ExploitationStates


async def back_to_main_handler(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.edit_text(text="Выберите пункт", reply_markup=main_keyboard())


# @dp.callback_query_handler(lambda query: query.data == "none", state=ProductStates.all_products)
async def paginate_handler(query: CallbackQuery, state: FSMContext):
    await query.answer(text="Здесь нет данных. Вы выбрали не ту страницу.", show_alert=True)