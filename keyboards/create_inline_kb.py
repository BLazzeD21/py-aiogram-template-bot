from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from math import ceil

from lexicon import LEXICON
from keyboards.profiles_callbackFactory import ProfilesCallbackFactory, ChangePageCallbackFactory


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


def create_profiles_keyboard(database: dict, page: int) -> InlineKeyboardMarkup:
    profiles_kb_builder = InlineKeyboardBuilder()
    profiles_buttons: list[InlineKeyboardButton] = []

    profiles = database.get_profiles()
    profiles_count: int = len(profiles)

    last_page: int = ceil(profiles_count / 6)
    start_profile = page * 6 - 6
    end_profile = start_profile + 6

    if (not profiles_count):
        profiles_buttons.append(InlineKeyboardButton(text=LEXICON["no_users"], callback_data="stub"))

    if (profiles_count <= 6 and profiles_count > 0):
        for user in profiles:
            callback_data = ProfilesCallbackFactory(user_id=str(user[1])).pack()
            text = LEXICON["profile_btn_text"].format(username=user[2])

            profiles_buttons.append(
                InlineKeyboardButton(text=text, callback_data=callback_data)
            )

    if profiles_count > 6:
        for user in profiles[start_profile:end_profile]:
            callback_data = ProfilesCallbackFactory(user_id=str(user[1])).pack()
            text = LEXICON["profile_btn_text"].format(username=user[2])

            profiles_buttons.append(
                InlineKeyboardButton(text=text, callback_data=callback_data)
            )
        if (page == 1):
            profiles_kb_builder.row(
                InlineKeyboardButton(
                    text=LEXICON["first_page"],
                    callback_data="stub",
                ),
                InlineKeyboardButton(
                    text=LEXICON["forward"],
                    callback_data=ChangePageCallbackFactory(page_number=str(page + 1)).pack(),
                ),
            )

        if (page == last_page):
            profiles_kb_builder.row(
                InlineKeyboardButton(
                    text=LEXICON["backward"],
                    callback_data=ChangePageCallbackFactory(page_number=str(page - 1)).pack(),
                ),
                InlineKeyboardButton(
                    text=LEXICON["last_page"],
                    callback_data="stub",
                ),
            )

        if (page != 1 and page != last_page):
            profiles_kb_builder.row(
                InlineKeyboardButton(
                    text=LEXICON["backward"],
                    callback_data=ChangePageCallbackFactory(page_number=str(page - 1)).pack(),
                ),
                InlineKeyboardButton(
                    text=LEXICON["forward"],
                    callback_data=ChangePageCallbackFactory(page_number=str(page + 1)).pack(),
                ),

            )

    profiles_kb_builder.row(*profiles_buttons, width=2)

    profiles_kb_builder.row(
        InlineKeyboardButton(text=LEXICON["back"], callback_data="back_btn")
    )

    return profiles_kb_builder.as_markup()
