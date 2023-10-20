from aiogram.types import Message
from aiogram.filters import BaseFilter


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message, configuration) -> bool:
        return message.from_user.id in configuration.tg_bot.admin_ids
