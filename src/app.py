from aiogram import executor
from asyncio import get_event_loop
from logging import basicConfig, INFO, warning

from src.loader import dp, bot
from src.commands.commands import set_up_commands

from src.handlers import main, admin, product, exploitation
from src.handlers import register_same_handlers
from src.middlewares.is_admin import AdminCheckerMiddleware

register_same_handlers(dp)


def on_startup():
    basicConfig(level=INFO)
    warning("Bot started")
    print("Connected to DB")


async def on_shutdown():
    warning("Shutting down..")
    await dp.storage.close()
    await dp.storage.wait_closed()
    warning("Bot down")


if __name__ == '__main__':
    dp.setup_middleware(AdminCheckerMiddleware(bot=bot))
    loop = get_event_loop()
    loop.run_until_complete(set_up_commands(bot_instance=bot))
    executor.start_polling(dp, on_startup=on_startup(), skip_updates=True)
