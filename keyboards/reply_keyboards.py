from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from lexicon import LEXICON

# ---------------------- Creating Buttons ----------------------

main_menu_button: KeyboardButton = KeyboardButton(text=LEXICON["main_menu_button"])
profile_button: KeyboardButton = KeyboardButton(text=LEXICON["profile_button"])
form_button: KeyboardButton = KeyboardButton(text=LEXICON["form_button"])
cancel_button: KeyboardButton = KeyboardButton(text=LEXICON["cancel_button"])

# ---------------------- Creating a keyboard menu ----------------------

main_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

main_btns: list[KeyboardButton] = [
    main_menu_button,
    profile_button,
    # form_button,
]

main_kb_builder.row(*main_btns, width=2)

main_kb: ReplyKeyboardMarkup = main_kb_builder.as_markup(
    resize_keyboard=True,
    one_time_keyboard=True,
    input_field_placeholder=LEXICON["main_kb_placeholder"],
)

# ---------------------- Creating a keyboard cancel ----------------------

cancel_kb_builder: ReplyKeyboardBuilder = ReplyKeyboardBuilder()

cancel_kb_builder.row(cancel_button, width=1)

cancel_kb: ReplyKeyboardMarkup = cancel_kb_builder.as_markup(
    resize_keyboard=True, one_time_keyboard=True
)
