from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message
from bson import ObjectId

from src.loader import dp, bot
from src.controllers import product_controller
from src.helpers.keyboards import main_keyboard, products_keyboard, back_keyboard, one_product_keyboard
from src.helpers.utils import Pagination, is_num
from src.helpers.format import product_format
from src.states.product import ProductStates


@dp.callback_query_handler(lambda query: query.data == "all_products", state=ProductStates.process)
async def all_products_handler(query: CallbackQuery, state: FSMContext):
    pagination = Pagination(data_type="PRODUCTS")
    paginated = await pagination.paginate(query={}, page=1, limit=6)
    await ProductStates.all_products.set()
    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(lambda query: query.data == "back", state=ProductStates.all_products)
async def back_from_all_products_handler(query: CallbackQuery, state: FSMContext):
    await ProductStates.process.set()
    await query.message.edit_text(text="Страница с техниками", reply_markup=products_keyboard())


@dp.callback_query_handler(lambda query: query.data == "delete", state=ProductStates.all_products)
async def back_from_all_products_handler(query: CallbackQuery, state: FSMContext):
    await ProductStates.process.set()
    await query.message.edit_text(text="Страница техники", reply_markup=products_keyboard())


@dp.callback_query_handler(lambda query: query.data in ["left#products#", "right#products#"], state=ProductStates.all_products)
async def pagination_products_handler(query: CallbackQuery, state: FSMContext):
    page = query.data.split("#")[2]
    pagination = Pagination(data_type="PRODUCTS")
    paginated = await pagination.paginate(query={}, page=int(page), limit=6)
    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(lambda query: query.data.startswith("sproduct_"), state=ProductStates.all_products)
async def get_product_handler(query: CallbackQuery, state: FSMContext):
    id = query.data.split("_")[1]

    product = await product_controller.get_one({"_id": ObjectId(id)})

    await ProductStates.one_product.set()

    await query.message.edit_text(text=product_format(product), reply_markup=one_product_keyboard(id))


@dp.callback_query_handler(lambda query: query.data == "back", state=ProductStates.one_product)
async def back_from_get_product_handler(query: CallbackQuery, state: FSMContext):
    pagination = Pagination(data_type="PRODUCTS")
    paginated = await pagination.paginate(query={}, page=1, limit=6)
    await ProductStates.all_products.set()
    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(lambda query: query.data.startswith("remove.product."), state=ProductStates.one_product)
async def remove_product_handler(query: CallbackQuery, state: FSMContext):
    id = query.data.split(".")[2]

    product = await product_controller.get_one({"_id": ObjectId(id)})

    query_data = dict(name=product['name'])

    if product['count'] - 1 == 0 and product['in_use'] != 0:
        await query.message.answer(f"{product['name']} используются. По этосму удалить это неаозможна")
        return

    if product['not_in_use'] - 1 == 0 and product['in_use'] > 0:
        await query.message.answer(f"{product['name']} используются. По этосму удалить это неаозможна")
        return

    if product['count'] - 1 == 0 and product['not_in_use'] - 1 == 0 and product['in_use'] == 0:
        await product_controller.delete(query_data)
        await ProductStates.process.set()
        await query.message.edit_text(
            text="Техника удален, так как его нет в складе.",
            reply_markup=products_keyboard()
        )
        return

    await product_controller.increment(query_data, {"count": -1, "not_in_use": -1})

    product = await product_controller.get_one(query_data)

    await query.message.edit_text(text=product_format(product), reply_markup=one_product_keyboard(id))


@dp.callback_query_handler(lambda query: query.data.startswith("add.product."), state=ProductStates.one_product)
async def add_product_handler(query: CallbackQuery, state: FSMContext):
    id = query.data.split(".")[2]

    product = await product_controller.get_one({"_id": ObjectId(id)})

    query_data = {"name": product['name']}

    await product_controller.increment(query_data, {"count": 1, "not_in_use": 1})

    product = await product_controller.get_one(query_data)

    await query.message.edit_text(text=product_format(product), reply_markup=one_product_keyboard(id))


@dp.callback_query_handler(lambda query: query.data.startswith("delete.product."), state=ProductStates.one_product)
async def delete_product_handler(query: CallbackQuery, state: FSMContext):
    id = query.data.split(".")[1]

    product = await product_controller.get_one({"_id": ObjectId(id)})

    if product.in_use > 0:
        await query.message.answer(
            text=f"Вы не можете удалить эту технику из базы, потому что {product['in_use']} этой техники взяты из склада"
        )

    await product_controller.delete({"_id": id})

    pagination = Pagination(data_type="PRODUCTS")
    paginated = pagination.paginate(query={}, page=1, limit=6)
    await ProductStates.all_products.set()
    await query.message.edit_text(text=paginated['message'], reply_markup=paginated['keyboard'])


@dp.callback_query_handler(lambda query: query.data == "add_product", state=ProductStates.process)
async def add_product_handler(query: CallbackQuery, state: FSMContext):
    await ProductStates.name.set()
    await query.message.edit_text(text="Отправьте название новой техники", reply_markup=back_keyboard())


@dp.callback_query_handler(lambda query: query.data == "back", state=ProductStates.name)
async def back_from_add_product_handler(query: CallbackQuery, state: FSMContext):
    await ProductStates.process.set()
    await query.message.edit_text(text="Страница техники", reply_markup=products_keyboard())


@dp.message_handler(state=ProductStates.name)
async def add_product_name_handler(message: Message, state: FSMContext):
    product = message.text

    if is_num(message.text):
        await message.answer("Отправьте название а не номер")
        return

    exist_product = await product_controller.get_one({"name": product})

    if exist_product is not None:
        await ProductStates.process.set()
        await message.edit_text("Такая ткхника уже есть в складе", reply_markup=products_keyboard())
        return

    message_for_delete = (await state.get_data())[f'message_for_delete_{message.from_user.id}']

    await ProductStates.count.set()

    await message.delete()

    await bot.delete_message(message.chat.id, message_for_delete)

    message_for_delete_1 = await message.answer(text=f"Отправьте сколько {product} есть в складе")

    async with state.proxy() as data:
        data[f'message_for_delete_1_{message.from_user.id}'] = message_for_delete_1.message_id
        data['new_product_name'] = product


@dp.message_handler(state=ProductStates.count)
async def add_product_handler(message: Message, state: FSMContext):
    if not is_num(message.text):
        await message.answer(text="Пожалуйста, отправьте правильный число")
        return

    data = await state.get_data()

    message_for_delete_1 = data[f'message_for_delete_1_{message.from_user.id}']
    product_name = data['new_product_name']

    product_data = dict(name=product_name, count=int(message.text), in_use=0, not_in_use=int(message.text), status='active')

    await product_controller.make(product_data)

    await ProductStates.process.set()

    await message.delete()
    await bot.delete_message(message.chat.id, message_for_delete_1)

    message_for_delete = await message.answer(text="Техника добавлена", reply_markup=products_keyboard())

    async with state.proxy() as data:
        data[f'message_for_delete_{message.from_user.id}'] = message_for_delete.message_id