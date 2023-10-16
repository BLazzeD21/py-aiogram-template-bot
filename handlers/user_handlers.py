from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, CommandStart
from aiogram import Router, F

from keyboards.reply_keyboards import main_kb
from keyboards.inline_keyboards import main_inline_kb, info_inline_kb
from lexicon import LEXICON

router = Router()

# ---------------------- Command handlers ----------------------

@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['/start'], reply_markup = main_kb)

@router.message(Command(commands='help'))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/help'], reply_markup = main_kb)

# ------------- Button handlers from ReplyKeyboards -------------

@router.message(F.text == LEXICON['first_button'])
async def process_first_button_press(message: Message):
    await message.answer(text=LEXICON['button_1_pressed'], reply_markup = main_inline_kb)

@router.message(F.text == LEXICON['second_button'])
async def process_second_button_press(message: Message):
    await message.answer(text=LEXICON['button_2_pressed'], reply_markup = main_inline_kb)

@router.message(F.text == LEXICON['third_button'])
async def process_third_button_press(message: Message):
    await message.answer(text=LEXICON['button_3_pressed'], reply_markup = main_inline_kb)

@router.message(F.text == LEXICON['fourth_button'])
async def process_fourth_button_press(message: Message):
    await message.answer(text=LEXICON['button_4_pressed'], reply_markup = main_inline_kb)

# ---------------- Button handlers from Callbacks ----------------

@router.callback_query(F.data == 'first_inline_button_pressed')
async def process_first_inline_button_press(callback: CallbackQuery):
    if callback.message.text != LEXICON['inline_button_1_pressed']:
        await callback.message.edit_text(
            text=LEXICON['inline_button_1_pressed'],
            reply_markup=info_inline_kb
        )
    await callback.answer(text=LEXICON['inline_button_1_pressed'], show_alert=True)

@router.callback_query(F.data == 'second_inline_button_pressed')
async def process_second_inline_button_press(callback: CallbackQuery):
    if callback.message.text != LEXICON['inline_button_2_pressed']:
        await callback.message.edit_text(
            text=LEXICON['inline_button_2_pressed'],
            reply_markup=info_inline_kb
        )
    await callback.answer(text=LEXICON['inline_button_2_pressed'], show_alert=True)

@router.callback_query(F.data == 'third_inline_button_pressed')
async def process_third_inline_button_press(callback: CallbackQuery):
    if callback.message.text != LEXICON['inline_button_3_pressed']:
        await callback.message.edit_text(
            text=LEXICON['inline_button_3_pressed'],
            reply_markup=info_inline_kb
        )
    await callback.answer(text=LEXICON['inline_button_3_pressed'])

@router.callback_query(F.data == 'fourth_inline_button_pressed')
async def process_fourth_inline_button_press(callback: CallbackQuery):
    if callback.message.text != LEXICON['inline_button_4_pressed']:
        await callback.message.edit_text(
            text=LEXICON['inline_button_4_pressed'],
            reply_markup=info_inline_kb
        )
    await callback.answer(text=LEXICON['inline_button_4_pressed'])

@router.callback_query(F.data == 'back_btn')
async def process_back_button_press(callback: CallbackQuery):
    await callback.message.edit_text(
        text=LEXICON['click'],
        reply_markup=main_inline_kb
    )
    await callback.answer()