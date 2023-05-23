from aiogram import Bot
from aiogram.types import Message
from aiogram.dispatcher.handler import CancelHandler
from aiogram.dispatcher.middlewares import BaseMiddleware
from src.controllers import admin_controller
from src.helpers.settings import ADMIN_IDS


class AdminCheckerMiddleware(BaseMiddleware):
    def __init__(self, bot: Bot):
        super().__init__()
        self.bot = bot

    async def on_process_message(self, message: Message, data, *args):
        admin = await admin_controller.get_one({"admin_id": message.from_user.id})

        if not admin and message.from_user.id not in ADMIN_IDS:
            await self.bot.send_message(chat_id=message.from_user.id, text='Not for you')
            raise CancelHandler()

        return
