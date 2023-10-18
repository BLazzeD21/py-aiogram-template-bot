from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon import LEXICON

# ---------------------- Creating Buttons ----------------------

main_menu_button = KeyboardButton(text=LEXICON['main_menu_button'])
profile_button = KeyboardButton(text=LEXICON['profile_button'])
registration_button = KeyboardButton(text=LEXICON['registration_button'])

cancel_button = KeyboardButton(text=LEXICON['cancel_button'])

# ---------------------- Creating a keyboard menu ----------------------

main_kb_builder = ReplyKeyboardBuilder()

main_btns: list[KeyboardButton] = [
    main_menu_button,
    profile_button,
    registration_button
  ]

main_kb_builder.row(*main_btns, width=2)

main_kb = main_kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder=LEXICON['main_kb_placeholder']
  )

cancel_kb_builder = ReplyKeyboardBuilder()

cancel_kb_builder.row(cancel_button, width=1)

cancel_kb = cancel_kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True
  )
