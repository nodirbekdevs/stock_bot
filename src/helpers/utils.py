from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from bson import ObjectId

from src.helpers.keyboards import back_keyboard
from src.controllers import admin_controller, exploitation_controller, exploitation_items_controller, product_controller
from src.helpers.format import exploitation_using_format, exploitation_used_format


class Pagination:
    def __init__(self, data_type: str):
        self.data_type = data_type

    async def paginate(self, query: dict, page: int, limit: int) -> dict:
        data, all_data, clause = [], [], ""

        offset = limit * (page - 1)

        if self.data_type == 'ADMINS':
            data = await admin_controller.get_pagination(query, offset, limit)
            all_data = await admin_controller.get_all(query)
            clause = 'admins'
        elif self.data_type == 'PRODUCTS':
            data = await product_controller.get_pagination(query, offset, limit)
            all_data = await product_controller.get_all(query)
            clause = 'products'
        elif self.data_type == 'EXPLOITATIONS':
            data = await exploitation_controller.get_pagination(query, offset, limit)
            all_data = await exploitation_controller.get_all(query)
            clause = "using_exploitation" if query['status'] == "using" else "used_exploitation"

        keyword, message, admin_name, keyboard = "", "", "", InlineKeyboardMarkup()

        if len(data) > 0:
            message = f'<b>Текущий: {offset + 1}-{len(data) + offset}, Общий: {len(all_data)}</b>\n\n'

            if self.data_type == 'ADMINS':
                message += f"<b>№</b>  <b>Имя</b>  <b>Username</b>  <b>Используют</b>\n"
            elif self.data_type == 'PRODUCTS':
                message += f"<b>№</b>  <b>Название</b>  <b>Все</b>  <b>Используемые</b>  <b>Неиспользованные</b>\n\n"
            elif self.data_type == 'EXPLOITATIONS':
                message += f"<b>№</b>  <b>Дающий</b>  <b>Получатель</b>\n"

            arr, inline_keyboard = [], []

            for i, single_data in enumerate(data, start=1):
                callback_data = ""

                if self.data_type == 'ADMINS':
                    callback_data = f"sadmin_{single_data['_id']}"
                elif self.data_type == 'PRODUCTS':
                    callback_data = f"sproduct_{single_data['_id']}"
                elif self.data_type == 'EXPLOITATIONS':
                    callback_data = f"sel.expo_{single_data['_id']}"

                    admin_name = (await admin_controller.get_one({"admin_id": single_data['admin']}))['first_name']

                obj = InlineKeyboardButton(text=f'{i}', callback_data=callback_data)

                arr.append(obj)

                if len(arr) % limit == 0:
                    keyboard.row(*arr)
                    arr = []

                if self.data_type == 'ADMINS':
                    message += f"<b>{i}.</b>  {single_data['first_name']}  {single_data['username']}  {'Да' if single_data['is_using'] else 'Нет'}\n"
                elif self.data_type == 'PRODUCTS':
                    message += f"<b>{i}.</b>  {single_data['name']}  {single_data['count']}  {single_data['in_use']}  {single_data['not_in_use']}\n"
                elif self.data_type == 'EXPLOITATIONS':
                    message += f"<b>{i}.</b>  {admin_name}  {single_data['being_given']}\n"
            keyboard.row(*arr)

            left_page_callback_data = f'left#{clause}#{page - 1}' if page != 1 else 'none'
            right_page_callback_data = f'right#{clause}#{page + 1}' if len(data) + offset != len(all_data) else 'none'

            inline_keyboard = [
                InlineKeyboardButton(text='⬅', callback_data=left_page_callback_data),
                InlineKeyboardButton(text='❌', callback_data="delete"),
                InlineKeyboardButton(text='➡', callback_data=right_page_callback_data)
            ]

            keyboard.row(*inline_keyboard)

            keyword = "YES"

        elif len(data) <= 0:
            keyboard = back_keyboard()
            message = "В базе ничего нет"
            keyword = "NO"

        return dict(keyword=keyword, message=message, keyboard=keyboard)


def is_num(number) -> bool:
    try:
        int(number)
        return True
    except ValueError:
        return False


async def send_message_to_group(exploitation_type, exploitation_id):
    admin_names, message = "", ""

    exploitation = await exploitation_controller.get_one({"_id": ObjectId(exploitation_id)})

    exploitation_items = await exploitation_items_controller.get_all(
        {"exploitation_id": exploitation['_id'], "status": exploitation['status']})

    if exploitation_type == 'using':
        admin_names = (await admin_controller.get_one({"admin_id": exploitation['admin']}))['first_name']
        message = exploitation_using_format(exploitation, admin_names, exploitation_items)
    elif exploitation_type == 'used':
        given = (await admin_controller.get_one({"admin_id": exploitation['admin']}))['first_name']
        received = (await admin_controller.get_one({"admin_id": exploitation['received']}))['first_name']
        admin_names = {"given": given, "received": received}
        message = exploitation_used_format(exploitation, admin_names, exploitation_items)

    return message


def status_translator(status):
    statuses = dict(process="В процессе", using="Используется", returned='Возвращенный')

    return statuses[status]


# if __name__ == '__main__':
#     pass
