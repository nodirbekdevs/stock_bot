from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from src.helpers.keyboards import main_keyboard


async def back_to_main_handler(query: CallbackQuery, state: FSMContext):
    await state.finish()
    await query.message.edit_text(text="Выберите пункт", reply_markup=main_keyboard())


async def paginate_handler(query: CallbackQuery, state: FSMContext):
    await query.answer(text="Здесь нет данных. Вы выбрали не ту страницу.", show_alert=True)