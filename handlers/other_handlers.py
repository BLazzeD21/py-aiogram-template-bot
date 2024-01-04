from aiogram.types import Message
from aiogram import Router
from aiogram.filters import StateFilter
from aiogram.fsm.state import default_state

from lexicon import LEXICON
from keyboards.reply_keyboards import cancel_kb

router: Router = Router()


@router.message(StateFilter(default_state))
async def other_messages_process(message: Message) -> None:
    await message.answer(text=LEXICON["other"])


@router.message(~StateFilter(default_state))
async def registering_other_process(message: Message) -> None:
    await message.answer(text=LEXICON["registering"], reply_markup=cancel_kb)
