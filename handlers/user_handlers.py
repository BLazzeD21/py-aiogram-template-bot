from aiogram.types import CallbackQuery, Message
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram import Router, F

from handlers.form_handlers import show_user_profile, registration_user_profile
from keyboards.reply_keyboards import main_kb
from keyboards.inline_keyboards import (
    main_inline_kb,
    info_inline_kb,
)
from keyboards.create_inline_kb import create_profiles_keyboard
from keyboards.profiles_callbackFactory import ProfilesCallbackFactory, ChangePageCallbackFactory
from lexicon import LEXICON, LEXICON_COMMANDS

router = Router()

# ---------------------- Command handlers ----------------------


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON["start_message"], reply_markup=main_kb, disable_web_page_preview=True)


@router.message(Command(commands="help"), StateFilter(default_state))
async def process_help_command(message: Message):
    help_message = LEXICON["help_message"]
    for key, value in LEXICON_COMMANDS.items():
        help_message += LEXICON["help_add"].format(command=key,description=value)

    await message.answer(text=help_message, reply_markup=main_kb)


# ------------- Button handlers from ReplyKeyboards -------------


@router.message(F.text == LEXICON["main_menu_button"], StateFilter(default_state))
async def process_main_button_press(message: Message):
    await message.answer(text=LEXICON["main_menu_button"], reply_markup=main_inline_kb)


# ---------------- Button handlers from Callbacks ----------------


@router.callback_query(F.data == "back_btn", StateFilter(default_state))
async def process_back_button_press(callback: CallbackQuery):
    await callback.message.answer(text=LEXICON["main_menu_button"], reply_markup=main_inline_kb)

    await callback.answer()
    await callback.message.delete()


@router.callback_query(F.data == "info_button", StateFilter(default_state))
async def process_info_button_press(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer(text=LEXICON["info_message"],reply_markup=info_inline_kb)
    await callback.answer()


@router.callback_query(F.data == "profile_button", StateFilter(default_state))
async def process_profile_button_press(callback: CallbackQuery, database):
    await callback.message.delete()

    user_id = callback.message.chat.id
    await show_user_profile(callback.message, user_id, database)

    await callback.answer()


@router.callback_query(F.data == "registration_button", StateFilter(default_state))
async def process_profile_button_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await registration_user_profile(callback.message, state)
    await callback.answer()


@router.callback_query(F.data.in_(["profiles_back_btn", "profiles_button"]), StateFilter(default_state))
async def process_profile_button_press(callback: CallbackQuery, database):
    profiles_kb = create_profiles_keyboard(database, 1)

    await callback.message.answer(text=LEXICON["select_account"], reply_markup=profiles_kb)

    await callback.message.delete()
    await callback.answer()

@router.callback_query(ChangePageCallbackFactory.filter())
async def process_category_press(callback: CallbackQuery, callback_data: ChangePageCallbackFactory, database):
    profiles_kb = create_profiles_keyboard(database, int(callback_data.page_number))

    await callback.message.answer(text=LEXICON["select_account"], reply_markup=profiles_kb)

    await callback.message.delete()
    await callback.answer()

@router.callback_query(ProfilesCallbackFactory.filter())
async def process_category_press(callback: CallbackQuery, callback_data: ProfilesCallbackFactory, database):
    user_id = int(callback_data.user_id)
    await show_user_profile(callback.message, user_id, database)

    await callback.message.delete()
    await callback.answer()

@router.callback_query(F.data == "stub", StateFilter(default_state))
async def no_users_press(callback: CallbackQuery):
    await callback.answer(text=LEXICON["stub"])
