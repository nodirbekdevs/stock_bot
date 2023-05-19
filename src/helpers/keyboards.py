from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def main_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Админы", callback_data=f'admins')],
        [InlineKeyboardButton(text="Техники", callback_data=f'products')],
        [InlineKeyboardButton(text="Эксплуатация", callback_data=f'exploitation')],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def admin_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Все админы", callback_data=f'all_admins')],
        [InlineKeyboardButton(text="Добавить админ", callback_data=f'add_admin')],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def products_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Все техники", callback_data=f'all_products')],
        [InlineKeyboardButton(text="Добавить технику", callback_data=f'add_product')],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def exploitation_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Техники", callback_data=f'products')],
        [InlineKeyboardButton(text="Подтверждение", callback_data=f'confirmation_products')],
        [InlineKeyboardButton(text="Используемые", callback_data=f'using_products')],
        [InlineKeyboardButton(text="Использванные", callback_data=f'used_products')],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def one_admin_keyboard(id) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Удалить", callback_data=f"delete.admin.{id}")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def one_product_keyboard(id) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(text="-", callback_data=f"remove.product.{id}"),
            InlineKeyboardButton(text="+", callback_data=f"add.product.{id}"),
        ],
        [InlineKeyboardButton(text="Удалить", callback_data=f"delete.product.{id}")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def one_exploitation_product_keyboard(id) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Добавить для использования", callback_data=f"add_use.product.{id}")],
        [InlineKeyboardButton(text="Назад", callback_data="back")],
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def one_exploitation_keyboard(id) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Удалить", callback_data=f"delete.exploitation.{id}")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def confirmation_exploitation_keyboard(products) -> InlineKeyboardMarkup:
    buttons = []

    for product in products:
        inline_keyboard = [
            InlineKeyboardButton(text='-', callback_data=f"minus.product.{product['_id']}"),
            InlineKeyboardButton(text='❌', callback_data=f"delete.exp_product.{product['_id']}"),
            InlineKeyboardButton(text='+', callback_data=f"plus.product.{product['_id']}")
        ]

        buttons.append(inline_keyboard)

    buttons.append(
        [
            InlineKeyboardButton(text="Подтверждение", callback_data=f"confirm.exploitation"),
            InlineKeyboardButton(text="Отмена", callback_data=f"cancel.exploitation"),
        ]
    )

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def one_using_exploitation_keyboard(id) -> InlineKeyboardMarkup:
    buttons = [
        [InlineKeyboardButton(text="Принятие", callback_data=f"return.exploitation.{id}")],
        [InlineKeyboardButton(text="Назад", callback_data="back")]
    ]

    return InlineKeyboardMarkup(inline_keyboard=buttons)


def back_keyboard() -> InlineKeyboardMarkup:
    buttons = [[
        InlineKeyboardButton(text="Назад", callback_data="back")
    ]]

    return InlineKeyboardMarkup(inline_keyboard=buttons)