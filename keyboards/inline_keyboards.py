from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.create_inline_kb import create_inline_kb

from lexicon import (
    LEXICON,
    MAIN_BUTTONS,
    SEX_BUTTONS,
    LINKS,
    SETTINGS,
    REGISTRATION,
    PROFILE,
)

# ---------------------- Creating Buttons ----------------------

aiogram_btn: InlineKeyboardButton = InlineKeyboardButton(
    text=LEXICON["aiogram"],
    url=LINKS["aiogram"],
)

github_btn: InlineKeyboardButton = InlineKeyboardButton(
    text=LEXICON["github"],
    url=LINKS["github"],
)

back_btn: InlineKeyboardButton = InlineKeyboardButton(
    text=LEXICON["back"],
    callback_data="back_btn",
)

# ------------------ Creating a keyboard menu ------------------

info_inline_kb: InlineKeyboardMarkup = InlineKeyboardMarkup(
    inline_keyboard=[
        [github_btn],
        [aiogram_btn],
        [back_btn],
    ]
)

# ------ Creating a keyboard menu using a special function ------

main_inline_kb: InlineKeyboardMarkup = create_inline_kb(2, **MAIN_BUTTONS)

sex_inline_kb: InlineKeyboardMarkup = create_inline_kb(2, **SEX_BUTTONS)

settings_inline_kb: InlineKeyboardMarkup = create_inline_kb(2, **SETTINGS)

registration_inline_kb: InlineKeyboardMarkup = create_inline_kb(2, **REGISTRATION)

profile_inline_kb: InlineKeyboardMarkup = create_inline_kb(2, **PROFILE)
