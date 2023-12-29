from typing import Any
from aiogram.types import Message
from aiogram.filters import BaseFilter

from config.config import Config
from models.methods import DatabaseMethods


class IsAdmin(BaseFilter):
    async def __call__(self, message: Message, configuration: Config) -> bool:
        return message.from_user.id in configuration.bot.admin_ids


class ExistProduct(BaseFilter):
    async def __call__(self, message: Message, database: DatabaseMethods) -> bool:
        return database.get_profile(message.from_user.id)
