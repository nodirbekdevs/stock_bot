from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from src.loader import dp, bot

from src.controllers import admin_controller
from src.helpers.settings import ADMIN_ID
from src.helpers.keyboards import main_keyboard, admin_keyboard, products_keyboard, exploitation_keyboard
from src.states.admin import AdminStates
from src.states.product import ProductStates
from src.states.exploitation import ExploitationStates


@dp.message_handler(commands='start')
async def cmd_start(message: Message, state: FSMContext):
    message_for_delete = await message.answer(text="Выберите пункт", reply_markup=main_keyboard())
    async with state.proxy() as data:
        data[f'message_for_delete_{message.from_user.id}'] = message_for_delete.message_id


@dp.callback_query_handler(lambda query: query.data == "admins")
async def admin_page(query: CallbackQuery, state: FSMContext):
    await AdminStates.process.set()
    await query.message.edit_text(text="Страница админов", reply_markup=admin_keyboard())


@dp.callback_query_handler(lambda query: query.data == "products")
async def product_page(query: CallbackQuery, state: FSMContext):
    await ProductStates.process.set()
    await query.message.edit_text(text="Страница техники", reply_markup=products_keyboard())


@dp.callback_query_handler(lambda query: query.data == "exploitation")
async def exploitation_page(query: CallbackQuery, state: FSMContext):
    await ExploitationStates.process.set()
    await query.message.edit_text(text="Страница эксплуатации", reply_markup=exploitation_keyboard())