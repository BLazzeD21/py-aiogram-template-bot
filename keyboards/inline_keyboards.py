from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.create_inline_kb import create_inline_kb, create_profiles_keyboard

from lexicon import LEXICON, MAIN_BUTTONS, SEX_BUTTONS, LINKS, BACK, BACK_PROFILES, REGISTRATION, PROFILE

# ---------------------- Creating Buttons ----------------------

aiogram_btn = InlineKeyboardButton(
    text=LEXICON["aiogram"],
    url=LINKS["aiogram"],
)

github_btn = InlineKeyboardButton(
    text=LEXICON["github"],
    url=LINKS["github"],
)

back_btn = InlineKeyboardButton(
    text=LEXICON["back"],
    callback_data="back_btn",
)

# ------------------ Creating a keyboard menu ------------------

info_inline_kb = InlineKeyboardMarkup(
    inline_keyboard=[
        [github_btn],
        [aiogram_btn],
        [back_btn],
    ]
)

# ------ Creating a keyboard menu using a special function ------


main_inline_kb = create_inline_kb(1, **MAIN_BUTTONS)

sex_inline_kb = create_inline_kb(1, **SEX_BUTTONS)

back_inline_kb = create_inline_kb(1, **BACK)

profiles_back_inline_kb = create_inline_kb(1, **BACK_PROFILES)

registration_inline_kb = create_inline_kb(1, **REGISTRATION)

profile_inline_kb = create_inline_kb(1, **PROFILE)
