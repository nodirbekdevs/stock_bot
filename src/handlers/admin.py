from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from bson import ObjectId

from src.loader import dp, bot
from src.controllers import admin_controller
from src.helpers.keyboards import admin_keyboard, one_admin_keyboard
from src.helpers.utils import Pagination, is_num
from src.helpers.format import admin_format
from src.states.admin import AdminStates


@dp.callback_query_handler(lambda query: query.data == "all_admins", state=AdminStates.process)
async def all_admins_handler(query: CallbackQuery, state: FSMContext):
    pagination = Pagination(data_type="ADMINS")
    paginated = await pagination.paginate(query=dict(status="active"), page=1, limit=6)
    await AdminStates.all_admins.set()
    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(lambda query: query.data == "back", state=AdminStates.all_admins)
async def back_from_all_admins_handler(query: CallbackQuery, state: FSMContext):
    await AdminStates.process.set()
    await query.message.edit_text(text="Страница админов", reply_markup=admin_keyboard())


@dp.callback_query_handler(lambda query: query.data == "delete", state=AdminStates.all_admins)
async def back_from_all_products_handler(query: CallbackQuery, state: FSMContext):
    await AdminStates.process.set()
    await query.message.edit_text(text="Страница админов", reply_markup=admin_keyboard())


@dp.callback_query_handler(
    lambda query: query.data.startswith("left#admins#") or query.data.startswith("right#admins#"),
    state=AdminStates.all_admins
    )
async def pagination_admins_handler(query: CallbackQuery, state: FSMContext):
    pagination = Pagination(data_type="ADMINS")
    paginated = await pagination.paginate(query=dict(status="active"), page=int(query.data.split("#")[2]), limit=6)
    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(lambda query: query.data.startswith("sadmin_"), state=AdminStates.all_admins)
async def get_admin_handler(query: CallbackQuery, state: FSMContext):
    id = query.data.split("_")[1]

    admin = await admin_controller.get_one({"_id": ObjectId(id)})

    await AdminStates.one_admin.set()

    await query.message.edit_text(text=admin_format(admin), reply_markup=one_admin_keyboard(id))


@dp.callback_query_handler(lambda query: query.data == "back", state=AdminStates.one_admin)
async def back_from_get_admin_handler(query: CallbackQuery, state: FSMContext):
    pagination = Pagination(data_type="ADMINS")
    paginated = await pagination.paginate(query=dict(status="active"), page=1, limit=6)
    await AdminStates.all_admins.set()
    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(lambda query: query.data.startswith("delete.admin."), state=AdminStates.one_admin)
async def delete_admin_handler(query: CallbackQuery, state: FSMContext):
    id = query.data.split(".")[2]

    admin = await admin_controller.get_one({"_id": ObjectId(id)})

    if admin['is_using']:
        await query.message.answer("Админ используют технику из склада. Так что вы не можете удалить")
        return

    await admin_controller.update({"_id": ObjectId(id)}, {"status": "inactive"})

    pagination = Pagination(data_type="ADMINS")
    paginated = await pagination.paginate(query=dict(status="active"), page=1, limit=6)
    await AdminStates.all_admins.set()
    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(lambda query: query.data == "add_admin", state=AdminStates.process)
async def add_admin_handler(query: CallbackQuery, state: FSMContext):
    await AdminStates.add.set()
    await query.message.edit_text(text="Отправьте telegram_id нового админа")


@dp.callback_query_handler(lambda query: query.data == "back", state=AdminStates.add)
async def back_from_add_admin_handler(query: CallbackQuery, state: FSMContext):
    await AdminStates.process.set()
    await query.message.edit_text(text="Страница админов", reply_markup=admin_keyboard())


@dp.message_handler(state=AdminStates.add)
async def add_admin_handler(message: Message, state: FSMContext):
    if not is_num(message.text):
        await message.answer(text="Пожалуйста, отправьте правильный telegram_id", reply_markup=admin_keyboard())
        return

    await AdminStates.process.set()

    if message.from_user.id == int(message.text):
        await message.answer(
            text="Отправьте telegrma id другого админа. Это telegram id пренадлежит вам.", reply_markup=admin_keyboard()
        )
        return

    exist_admin = await admin_controller.get_one({"admin_id": int(message.text), "status": {"$in": ['active', 'inactive']}})

    if exist_admin:
        message_text = ""

        if exist_admin['status'] == 'inactive':
            await admin_controller.update({"admin_id": int(message.text)}, {"status": "active"})
            message_text = "Новый админ добален"

        if exist_admin['status'] == 'active':
            message_text = "Этот админ уже добавлен к базе"

        await message.answer(message_text, reply_markup=admin_keyboard())
        return

    try:
        admin = await bot.get(chat_id=int(message.text))
    except:
        await message.answer("Отправьте правильное telegrma id", reply_markup=admin_keyboard())
        return

    admin_data = dict(
        admin_id=admin['id'],
        first_name=admin['first_name'],
        last_name=admin['last_name'],
        username=admin['username'],
        is_using=False,
        status='active',
    )

    await admin_controller.make(admin_data)

    await bot.send_message(chat_id=admin['id'], text="Вы успешно добавлены для пользования склада.\n Нажмите /start")

    await message.delete()

    await message.answer(text="Новый админ добален", reply_markup=admin_keyboard())
