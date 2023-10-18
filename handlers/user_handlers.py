from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router, F


from keyboards.reply_keyboards import main_kb
from keyboards.inline_keyboards import main_inline_kb, info_inline_kb
from lexicon import LEXICON

router = Router()

# ---------------------- Command handlers ----------------------

@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON['/start'], reply_markup = main_kb)

@router.message(Command(commands='help'), StateFilter(default_state))
async def process_help_command(message: Message):
    await message.answer(text=LEXICON['/help'], reply_markup = main_kb)

# ------------- Button handlers from ReplyKeyboards -------------

@router.message(F.text == LEXICON['main_menu_button'], StateFilter(default_state))
async def process_first_button_press(message: Message):
    await message.answer(text=LEXICON['main_menu_button'], reply_markup = main_inline_kb)

# ---------------- Button handlers from Callbacks ----------------

@router.callback_query(F.data == 'back_btn', StateFilter(default_state))
async def process_back_button_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['main_menu_button'], reply_markup = main_inline_kb)
    await callback.answer()


@router.callback_query(F.data == 'info_button', StateFilter(default_state))
async def process_back_button_press(callback: CallbackQuery):
    await callback.message.edit_text(text=LEXICON['info'], reply_markup = info_inline_kb)
    await callback.answer()


# @router.callback_query(F.data == 'first_inline_button_pressed', StateFilter(default_state))
# async def process_first_inline_button_press(callback: CallbackQuery):
#     if callback.message.text != LEXICON['inline_button_1_pressed']:
#         await callback.message.edit_text(
#             text=LEXICON['inline_button_1_pressed'],
#             reply_markup=info_inline_kb
#         )
#     