from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from src.controllers import admin_controller
from src.helpers.settings import ADMIN_IDS, ADMIN_ID


class AdminCheckerMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def on_process_message(self, message: Message, data, *args):
        core_admin = await admin_controller.get_one({"admin_id": ADMIN_ID, "status": "process"})

        if not core_admin:
            chat_data = await self.bot.get_chat(chat_id=ADMIN_ID)

            admin_data = dict(
                admin_id=chat_data.id,
                first_name=chat_data.first_name,
                last_name=chat_data.last_name,
                username=chat_data.username
            )

            await admin_controller.make(admin_data)

        admin = await admin_controller.get_one({"admin_id": message.from_user.id, "status": {"$in": ['process', 'active']}})

        if admin is None and message.from_user.id not in ADMIN_IDS:
            await self.bot.send_message(chat_id=message.from_user.id, text='Not for you')
            raise CancelHandler()

        return
