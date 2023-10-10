from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from utils.get_admins import get_admin_ids
from filters.filters import IsAdmin
from keyboards.reply_keyboards import main_kb
from lexicon import LEXICON_EN

router = Router()
admin_ids = get_admin_ids()

# ---------------------- Command handlers ----------------------

@router.message(Command(commands='admin'), IsAdmin(admin_ids))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_EN['admin'], reply_markup = main_kb)