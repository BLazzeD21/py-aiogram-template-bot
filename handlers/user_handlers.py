from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram import Router, F
from models.methods import DatabaseMethods

from handlers.form_handlers import (
    show_user_profile,
    registration_user_profile,
    show_another_users_profile,
)
from keyboards.reply_keyboards import main_kb
from keyboards.inline_keyboards import (
    main_inline_kb,
    info_inline_kb,
)
from keyboards.create_inline_kb import create_profiles_keyboard
from keyboards.profiles_callbackFactory import (
    ProfilesCallbackFactory,
    ChangePageCallbackFactory,
)
from lexicon import LEXICON, LEXICON_COMMANDS

router: Router = Router()

# ---------------------- Command handlers ----------------------


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message) -> None:
    await message.answer(
        text=LEXICON["start_message"],
        reply_markup=main_kb,
        disable_web_page_preview=True,
    )


@router.message(Command(commands="help"), StateFilter(default_state))
async def process_help_command(message: Message) -> None:
    help_message: str = LEXICON["help_message"]

    for key, value in LEXICON_COMMANDS.items():
        help_message += LEXICON["help_add"].format(command=key, description=value)

    await message.answer(text=help_message, reply_markup=main_kb)


# ------------- Button handlers from ReplyKeyboards -------------


@router.message(F.text == LEXICON["main_menu_button"], StateFilter(default_state))
async def process_main_button_press(message: Message) -> None:
    await message.answer(text=LEXICON["main_menu_button"], reply_markup=main_inline_kb)


# ---------------- Button handlers from Callbacks ----------------


@router.callback_query(F.data == "back_btn", StateFilter(default_state))
async def process_back_button_press(callback: CallbackQuery) -> None:
    await callback.message.delete()

    await callback.message.answer(
        text=LEXICON["main_menu_button"], reply_markup=main_inline_kb
    )

    await callback.answer()


@router.callback_query(F.data == "info_button", StateFilter(default_state))
async def process_info_button_press(callback: CallbackQuery) -> None:
    await callback.message.delete()

    await callback.message.answer(
        text=LEXICON["info_message"], reply_markup=info_inline_kb
    )
    await callback.answer()


@router.callback_query(F.data == "profile_button", StateFilter(default_state))
async def process_profile_button_press(
    callback: CallbackQuery, database: DatabaseMethods
) -> None:
    await callback.message.delete()

    user_id: int = callback.message.chat.id
    await show_user_profile(callback.message, user_id, database)

    await callback.answer()


@router.callback_query(F.data == "registration_button", StateFilter(default_state))
async def process_registration_button_press(
    callback: CallbackQuery, state: FSMContext
) -> None:
    await callback.message.delete()

    await registration_user_profile(callback.message, state)

    await callback.answer()


@router.callback_query(
    F.data.in_(["profiles_back_btn", "profiles_button"]), StateFilter(default_state)
)
async def process_profile_call(
    callback: CallbackQuery, database: DatabaseMethods
) -> None:
    await callback.message.delete()

    profiles_kb: InlineKeyboardMarkup = create_profiles_keyboard(database, 1)

    await callback.message.answer(
        text=LEXICON["select_account"], reply_markup=profiles_kb
    )
    await callback.answer()


@router.callback_query(ChangePageCallbackFactory.filter())
async def change_page_press(
    callback: CallbackQuery,
    callback_data: ChangePageCallbackFactory,
    database: DatabaseMethods,
) -> None:
    profiles_kb: InlineKeyboardMarkup = create_profiles_keyboard(
        database, int(callback_data.page_number)
    )

    await callback.answer()

    method: bool = callback_data.method_answer

    if method:
        await callback.message.delete()

        await callback.message.answer(
            text=LEXICON["select_account"], reply_markup=profiles_kb
        )
        return

    await callback.message.edit_text(
        text=LEXICON["select_account"], reply_markup=profiles_kb
    )


@router.callback_query(ProfilesCallbackFactory.filter())
async def show_profiles_press(
    callback: CallbackQuery,
    callback_data: ProfilesCallbackFactory,
    database: DatabaseMethods,
) -> None:
    user_id: int = callback_data.user_id
    page: int = callback_data.page_number

    await show_another_users_profile(callback, user_id, database, page)


@router.callback_query(F.data == "stub", StateFilter(default_state))
async def no_users_press(callback: CallbackQuery) -> None:
    await callback.answer(text=LEXICON["stub"])
