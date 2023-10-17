from aiogram.types import Message
from aiogram.filters import Command
from aiogram import Router

from filters.filters import IsAdmin
from keyboards.reply_keyboards import main_kb
from lexicon import LEXICON

router = Router()

# ---------------------- Command handlers ----------------------

@router.message(Command(commands='admin'), IsAdmin())
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['admin'], reply_markup = main_kb)