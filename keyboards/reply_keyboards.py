from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon import LEXICON

# ---------------------- Creating Buttons ----------------------

first_button = KeyboardButton(text=LEXICON['first_button'])
second_button = KeyboardButton(text=LEXICON['second_button'])
third_button = KeyboardButton(text=LEXICON['third_button'])
fourth_button = KeyboardButton(text=LEXICON['fourth_button'])

# ---------------------- Creating a keyboard menu ----------------------

main_kb_builder = ReplyKeyboardBuilder()

main_btns: list[KeyboardButton] = [
    first_button,
    second_button,
    third_button,
    fourth_button
  ]

main_kb_builder.row(*main_btns, width=2)

main_kb = main_kb_builder.as_markup(resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder=LEXICON['main_kb_placeholder']
  )
