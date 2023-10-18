from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state
from aiogram.fsm.context import FSMContext

from lexicon import LEXICON

router = Router()

@router.message(StateFilter(default_state))
async def send_echo(message: Message):
  await message.answer(text=LEXICON['other'])