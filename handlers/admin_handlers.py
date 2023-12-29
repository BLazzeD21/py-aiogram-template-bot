from aiogram.types import Message
from aiogram import Router
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import default_state

from filters.filters import IsAdmin
from keyboards.reply_keyboards import main_kb
from lexicon import LEXICON

router: Router = Router()

# ---------------------- Command handlers ----------------------


@router.message(Command(commands="admin"), IsAdmin(), StateFilter(default_state))
async def process_admin_command(message: Message) -> None:
    await message.answer(text=LEXICON["admin"], reply_markup=main_kb)
