
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, chat
from src.bot import bot
from src.config import Config
from aiogram import Router
from aiogram import F

router = Router()

@router.message(F.message.chat.type=='supergroup')
async def save_message(message: Message):
    print(message.text)