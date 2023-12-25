from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from lexicon import LEXICON
from keyboards.profiles_callbackFactory import ProfilesCallbackFactory

def create_inline_kb(width: int, *args: str, **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder = InlineKeyboardBuilder()

    buttons: list[InlineKeyboardButton] = []

    if args:
        for button in args:
            buttons.append(
                InlineKeyboardButton(
                    text=LEXICON[button] if button in LEXICON else button,
                    callback_data=button,
                )
            )

    if kwargs:
        for button, text in kwargs.items():
            buttons.append(InlineKeyboardButton(text=text, callback_data=button))

    kb_builder.row(*buttons, width=width)

    return kb_builder.as_markup()


def create_profiles_keyboard(database: dict) -> InlineKeyboardMarkup:
    profiles_kb_builder = InlineKeyboardBuilder()
    profiles = database.get_profiles()
    if(profiles):
        for user in profiles:
            callback_data = ProfilesCallbackFactory(user_id=str(user[1])).pack()
            text = f'{user[2]}\'s profile'

            profiles_kb_builder.row(
                InlineKeyboardButton(text=text, callback_data=callback_data)
            )
    else:
        profiles_kb_builder.row(
                InlineKeyboardButton(text='No', callback_data='no_users')
            )

    profiles_kb_builder.row(
        InlineKeyboardButton(text=LEXICON["back"], callback_data="back_btn")
    )

    return profiles_kb_builder.as_markup()
