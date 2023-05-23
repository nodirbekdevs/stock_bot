from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from src.controllers import admin_controller, product_controller, exploitation_controller
from src.helpers.keyboards import back_keyboard


class Pagination:
    def __init__(self, data_type: str):
        self.data_type = data_type

    async def paginate(self, query: dict, page: int, limit: int, type: str = "") -> dict:
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

                if len(arr) % 6 == 0:
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


if __name__ == '__main__':
    pass
