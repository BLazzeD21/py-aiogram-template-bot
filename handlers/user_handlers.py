from aiogram.types import CallbackQuery, Message, InlineKeyboardMarkup
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.state import default_state
from aiogram import Router, F

from models.methods import DatabaseMethods
from utils import show_user_profile, show_another_users_profile
from keyboards.reply_keyboards import main_kb
from keyboards.inline_keyboards import main_inline_kb, info_inline_kb
from keyboards.create_inline_kb import create_profiles_keyboard
from keyboards.profiles_callbackFactory import (
    ProfilesCallbackFactory,
    ChangePageCallbackFactory,
)
from lexicon import LEXICON, LEXICON_COMMANDS

router: Router = Router()


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


@router.message(F.text == LEXICON["main_menu_button"], StateFilter(default_state))
async def process_main_button_press(message: Message) -> None:
    await message.answer(text=LEXICON["main_menu_button"], reply_markup=main_inline_kb)


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


@router.message(F.text == LEXICON["profile_button"], StateFilter(default_state))
async def process_show_profile(message: Message, database: DatabaseMethods) -> None:
    user_id: int = message.from_user.id
    await show_user_profile(message, user_id, database)


@router.callback_query(F.data == "delete_profile", StateFilter(default_state))
async def process_delete_profile_press(
    callback: CallbackQuery, database: DatabaseMethods
) -> None:
    user_id: int = callback.message.chat.id
    await callback.message.delete()

    try:
        await database.connect()
        await database.delete_profile(user_id)
        await callback.message.answer_sticker(
            LEXICON["profile_deleted_sticker"], reply_markup=main_kb
        )
        await callback.message.answer(text=LEXICON["profile_deleted"])
    except:
        await callback.message.answer(text=LEXICON["db_error"], reply_markup=main_kb)
    finally:
        await database.close()


@router.callback_query(F.data == "profile_button", StateFilter(default_state))
async def process_profile_button_press(
    callback: CallbackQuery, database: DatabaseMethods
) -> None:
    await callback.message.delete()

    user_id: int = callback.message.chat.id
    await show_user_profile(callback.message, user_id, database)

    await callback.answer()


@router.callback_query(
    F.data.in_(["profiles_back_btn", "profiles_button"]), StateFilter(default_state)
)
async def process_profile_call(
    callback: CallbackQuery, database: DatabaseMethods
) -> None:
    await callback.message.delete()
    try:
        await database.connect()
        profiles: list[tuple] = await database.get_profiles()

        profiles_kb: InlineKeyboardMarkup = create_profiles_keyboard(profiles, 1)

        await callback.message.answer(
            text=LEXICON["select_account"], reply_markup=profiles_kb
        )
        await callback.answer()
    except:
        await callback.message.answer(text=LEXICON["db_error"], reply_markup=main_kb)
    finally:
        await database.close()


@router.callback_query(ChangePageCallbackFactory.filter())
async def change_page_press(
    callback: CallbackQuery,
    callback_data: ChangePageCallbackFactory,
    database: DatabaseMethods,
) -> None:
    user_id = int(callback_data.page_number)
    try:
        await database.connect()
        profiles: list[tuple] = await database.get_profiles()

        profiles_kb: InlineKeyboardMarkup = create_profiles_keyboard(profiles, user_id)

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
    except:
        await callback.message.answer(text=LEXICON["db_error"], reply_markup=main_kb)
    finally:
        await database.close()


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
