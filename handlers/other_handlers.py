from aiogram.types import Message
from aiogram import Router

from lexicon import LEXICON_EN

router = Router()

@router.message()
async def send_echo(message: Message):
  await message.answer(text=LEXICON_EN['other'])