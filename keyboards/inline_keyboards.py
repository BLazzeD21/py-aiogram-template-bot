from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.create_inline_kb import create_inline_kb

from lexicon import LEXICON_EN, MAIN_BUTTONS, LINKS

# ---------------------- Creating Buttons ----------------------

aiogram_btn = InlineKeyboardButton(
        text=LEXICON_EN['aiogram'],
        url=LINKS['aiogram'],
    )

github_btn = InlineKeyboardButton(
        text=LEXICON_EN['github'],
        url=LINKS['github'],
    )

back_btn = InlineKeyboardButton(
        text=LEXICON_EN['back'],
        callback_data="back_btn",
    )

# ------------------ Creating a keyboard menu ------------------

info_inline_kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [aiogram_btn, github_btn],
            [back_btn],
        ]
    )

# ------ Creating a keyboard menu using a special function ------


main_inline_kb = create_inline_kb(2, **MAIN_BUTTONS)
