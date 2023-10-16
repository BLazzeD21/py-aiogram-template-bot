from aiogram.types import Message
from aiogram import Router

from lexicon import LEXICON

router = Router()

@router.message()
async def send_echo(message: Message):
  await message.answer(text=LEXICON['other'])