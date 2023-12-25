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
    back_inline_kb,
    profiles_back_inline_kb,
)
from keyboards.create_inline_kb import create_profiles_keyboard
from keyboards.profiles_callbackFactory import ProfilesCallbackFactory
from lexicon import LEXICON, LEXICON_COMMANDS
from models import user_dict

router = Router()

# ---------------------- Command handlers ----------------------


@router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message):
    await message.answer(text=LEXICON["/start"], reply_markup=main_kb)


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
    await callback.message.edit_text(text=LEXICON["info"], reply_markup=info_inline_kb)
    await callback.answer()


@router.callback_query(F.data == "profile_button", StateFilter(default_state))
async def process_profile_button_press(callback: CallbackQuery):
    await callback.message.delete()
    user_id = callback.from_user.id
    await show_user_profile(callback.message, user_id)
    await callback.answer()


@router.callback_query(F.data == "registration_button", StateFilter(default_state))
async def process_profile_button_press(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await registration_user_profile(callback.message, state)
    await callback.answer()


@router.callback_query(F.data.in_(["profiles_back_btn", "profiles_button"]), StateFilter(default_state))
async def process_profile_button_press(callback: CallbackQuery):
    profiles_kb = create_profiles_keyboard(user_dict)

    await callback.message.answer(text=LEXICON["select_account"], reply_markup=profiles_kb)

    await callback.message.delete()
    await callback.answer()


@router.callback_query(ProfilesCallbackFactory.filter())
async def process_category_press(callback: CallbackQuery, callback_data: ProfilesCallbackFactory):
    user_id = int(callback_data.user_id)
    user_data = LEXICON["get_profile_data"].format(
        user_id=user_id,
        username=user_dict[user_id]["username"],
        name=user_dict[user_id]["name"],
        age=user_dict[user_id]["age"],
        gender=user_dict[user_id]["gender"],
        description=user_dict[user_id]["description"]
    )

    await callback.message.answer_photo(
        photo=user_dict[user_id]["photo_id"],
        caption=user_data,
        reply_markup=profiles_back_inline_kb,
    )

    await callback.message.delete()
    await callback.answer()
