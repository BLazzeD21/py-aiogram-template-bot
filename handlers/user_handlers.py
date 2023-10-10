from aiogram.types import Message
from aiogram.filters import Command, CommandStart
from aiogram import Router, F

from keyboards.reply_keyboards import main_kb
from lexicon.lexicon_ru import LEXICON_RU

router = Router()

# ---------------------- Command handlers ----------------------

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup = main_kb)

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON_RU['/help'], reply_markup = main_kb)

# ------------- Button handlers from ReplyKeyboards -------------

@router.message(F.text == LEXICON_RU['first_button'])
async def process_help_command(message: Message):
    await message.answer(text="Action after clicking <i>button 1</i>", reply_markup = main_kb)

@router.message(F.text == LEXICON_RU['second_button'])
async def process_help_command(message: Message):
    await message.answer(text="Action after clicking <i>button 2</i>", reply_markup = main_kb)

@router.message(F.text == LEXICON_RU['third_button'])
async def process_help_command(message: Message):
    await message.answer(text="Action after clicking <i>button 3</i>", reply_markup = main_kb)

@router.message(F.text == LEXICON_RU['fourth_button'])
async def process_help_command(message: Message):
    await message.answer(text="Action after clicking <i>button 4</i>", reply_markup = main_kb)

