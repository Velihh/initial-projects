from typing import Union

from aiogram.filters import BaseFilter
from aiogram.types import Message
from config import Config


class ChatTypeFilter(BaseFilter):  # [1]
    def __init__(self, chat_type: Union[str, list]): # [2]
        self.chat_type = chat_type

    async def __call__(self, message: Message) -> bool:  # [3]
        if isinstance(self.chat_type, str):
            return message.chat.type == self.chat_type
        else:
            try:
                return message.chat.type in self.chat_type
            except:
                return False

class IsTrueContact(BaseFilter):
    async def __call__(self, message: Message):
        if message.from_user.id in Config.admins_id:
            return True
        else:
            return False