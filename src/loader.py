from aiogram import Bot, Dispatcher
from aiogram.types import ParseMode
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from src.helpers.settings import TOKEN, TIME_OUT

bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML, timeout=TIME_OUT)
dp = Dispatcher(bot, storage=MemoryStorage())