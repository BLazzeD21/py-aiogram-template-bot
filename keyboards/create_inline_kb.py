from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder
from math import ceil
from models.methods import DatabaseMethods

from lexicon import LEXICON
from keyboards.profiles_callbackFactory import (
    ProfilesCallbackFactory,
    ChangePageCallbackFactory,
)


def create_inline_kb(width: int, *args: str, **kwargs: str) -> InlineKeyboardMarkup:
    kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

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


def create_profiles_keyboard(
    database: DatabaseMethods, page: int
) -> InlineKeyboardMarkup:
    profiles_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()
    profiles_buttons: list[InlineKeyboardButton] = []

    profiles: list[tuple] = database.get_profiles()

    profiles_count: int = len(profiles)
    profiles_on_page: int = 4
    pages_count: int = ceil(profiles_count / profiles_on_page)

    start_profile: int = page * profiles_on_page - profiles_on_page
    end_profile: int = start_profile + profiles_on_page

    if not profiles_count:
        profiles_buttons.append(
            InlineKeyboardButton(text=LEXICON["no_users"], callback_data="stub")
        )

    if profiles_count <= profiles_on_page and profiles_count > 0:
        for user in profiles:
            callback_data: ProfilesCallbackFactory = ProfilesCallbackFactory(
                user_id=str(user[1]), page_number=str(page)
            ).pack()
            text: str = LEXICON["profile_btn_text"].format(username=user[2])

            profiles_buttons.append(
                InlineKeyboardButton(text=text, callback_data=callback_data)
            )

    if profiles_count > profiles_on_page:
        for user in profiles[start_profile:end_profile]:
            callback_data: ProfilesCallbackFactory = ProfilesCallbackFactory(
                user_id=str(user[1]), page_number=str(page)
            ).pack()
            text: str = LEXICON["profile_btn_text"].format(username=user[2])

            profiles_buttons.append(
                InlineKeyboardButton(text=text, callback_data=callback_data)
            )
        if page == 1:
            profiles_kb_builder.row(
                InlineKeyboardButton(
                    text=LEXICON["first_page"],
                    callback_data="stub",
                ),
                InlineKeyboardButton(
                    text=LEXICON["forward"],
                    callback_data=ChangePageCallbackFactory(
                        page_number=str(page + 1),
                        method_answer=False,
                    ).pack(),
                ),
            )

        if page == pages_count:
            profiles_kb_builder.row(
                InlineKeyboardButton(
                    text=LEXICON["backward"],
                    callback_data=ChangePageCallbackFactory(
                        page_number=str(page - 1),
                        method_answer=False,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=LEXICON["last_page"],
                    callback_data="stub",
                ),
            )

        if page != 1 and page != pages_count:
            profiles_kb_builder.row(
                InlineKeyboardButton(
                    text=LEXICON["backward"],
                    callback_data=ChangePageCallbackFactory(
                        page_number=str(page - 1),
                        method_answer=False,
                    ).pack(),
                ),
                InlineKeyboardButton(
                    text=f"{page} / {pages_count}",
                    callback_data="stub",
                ),
                InlineKeyboardButton(
                    text=LEXICON["forward"],
                    callback_data=ChangePageCallbackFactory(
                        page_number=str(page + 1),
                        method_answer=False,
                    ).pack(),
                ),
            )

    profiles_kb_builder.row(*profiles_buttons, width=1)

    profiles_kb_builder.row(
        InlineKeyboardButton(text=LEXICON["back"], callback_data="back_btn")
    )

    return profiles_kb_builder.as_markup()


def create_back_to_page(page: int) -> InlineKeyboardMarkup:
    back_kb_builder: InlineKeyboardBuilder = InlineKeyboardBuilder()

    back_kb_builder.row(
        InlineKeyboardButton(
            text=LEXICON["back_profiles"],
            callback_data=ChangePageCallbackFactory(
                page_number=str(page),
                method_answer=True,
            ).pack(),
        ),
        InlineKeyboardButton(text=LEXICON["back"], callback_data="back_btn"),
    )

    return back_kb_builder.as_markup()
