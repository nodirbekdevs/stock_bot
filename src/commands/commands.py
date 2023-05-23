from aiogram import Bot
from aiogram.types import BotCommand


commands = [
    BotCommand(command="start", description="Запустить")
]


async def set_up_commands(bot_instance: Bot) -> None:
    await bot_instance.delete_my_commands()

    await bot_instance.set_my_commands(commands=commands)