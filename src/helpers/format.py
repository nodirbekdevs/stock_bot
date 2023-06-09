# from .utils import status_translator


def admin_format(admin):
    information = "Информация администратора\n\n"

    # information += f"№ - {admin['id']}\n"
    information += f"Имя - {admin['first_name']}\n"
    information += f"Фамилия - {admin['last_name']}\n"
    information += f"Username - @{admin['username']}\n"
    information += f"Использует - {'Да' if admin['is_using'] else 'Нет'}\n"

    return information


def product_format(product):
    information = "Информация техники\n\n"

    # information += f"№ - {product['id']}\n"
    information += f"Название - {product['name']}\n"
    information += f"Все - {product['count']}\n"
    information += f"Используемые - {product['in_use']}\n"
    information += f"Неиспользованные - {product['not_in_use']}\n"

    return information


def confirmation_exploitation_format(exploitation, admin_name, products):
    information = "Информация о пользования с техниками\n\n"

    information += f"Отдал - {admin_name}\n\n"

    information += "<b>Техники</b>\n"

    for product in products:
        information += f"Название - {product['product_name']}\n"
        information += f"Число - {product['quantity']}\n\n"

    # information += f"Статус - {status_translator(exploitation['status'])}\n"
    information += f"Статус - В процессе\n"

    return information


def exploitation_using_format(exploitation, admin_name, products):
    information = "Информация о пользования с техниками\n\n"

    information += f"Отдал - {admin_name}\n"
    information += f"Кому - {exploitation['being_given']}\n"

    information += "\n<b>Техники</b>\n"

    for product in products:
        information += f"Название - {product['product_name']}\n"
        information += f"Число - {product['quantity']}\n\n"

    information += f"Время получения - {exploitation['given_at'].strftime('%d.%m.%Y %H:%M')}\n\n"

    # information += f"Статус - {status_translator(exploitation['status'])}"
    information += f"Статус - Используется"

    return information


def exploitation_used_format(exploitation, admin_names, products):
    information = "Информация о пользования с техниками\n\n"

    information += f"Отдал - {admin_names['given']}\n"
    information += f"Кому - {exploitation['being_given']}\n"
    information += f"Принял - {admin_names['received']}\n"

    information += "\n<b>Техники</b>\n"

    for product in products:
        information += f"Название - {product['product_name']}\n"
        information += f"Число - {product['quantity']}\n\n"

    information += f"Время получения - {exploitation['given_at'].strftime('%d.%m.%Y %H:%M')}\n"
    information += f"Время выдачи - {exploitation['returned_at'].strftime('%d.%m.%Y %H:%M')}\n\n"

    # information += f"Статус - {status_translator(exploitation['status'])}"
    information += f"Статус - Возвращенный"

    return information