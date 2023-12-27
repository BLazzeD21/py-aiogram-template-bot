from aiogram.types import CallbackQuery, Message, PhotoSize
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram import Router, F

from keyboards.reply_keyboards import main_kb, cancel_kb
from keyboards.inline_keyboards import (
    sex_inline_kb,
    registration_inline_kb,
    back_inline_kb,
)
from keyboards.create_inline_kb import create_back_to_page
from lexicon import LEXICON
from states import FSMRegistration


router = Router()

# ------------------------- Functions -------------------------


async def send_profile(message: Message, user_data, keyboard):
    caption = LEXICON["get_profile_data"].format(
        user_id=user_data[1],
        username=user_data[2],
        name=user_data[3],
        age=user_data[4],
        gender=user_data[5],
        description=user_data[6],
    )
    await message.answer_photo(
        photo=user_data[7],
        caption=caption,
        reply_markup=keyboard,
    )


async def show_user_profile(message: Message, user_id, database):
    user_data = database.get_profile(user_id)

    if user_data:
        await send_profile(message, user_data, back_inline_kb)
    else:
        await message.answer(
            text=LEXICON["not_registered"], reply_markup=registration_inline_kb
        )

async def show_another_users_profile(callback: CallbackQuery, user_id, database, page: str):
    user_data = database.get_profile(user_id)
    keyboard = create_back_to_page(page)
    if user_data:
        await callback.message.delete()
        await send_profile(callback.message, user_data, keyboard)
    else:
        await callback.answer(text=LEXICON["not_exist"])


async def registration_user_profile(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["enter_name"], reply_markup=cancel_kb)
    await state.set_state(FSMRegistration.fill_name)


# ---------------------- Command handlers ----------------------


@router.message(Command(commands="registration"), StateFilter(default_state))
@router.message(F.text == LEXICON["registration_button"], StateFilter(default_state))
async def process_registration_command(message: Message, state: FSMContext):
    await registration_user_profile(message, state)


@router.message(Command(commands="cancel"), StateFilter(default_state))
@router.message(F.text == LEXICON["cancel_button"], StateFilter(default_state))
async def process_cancel_command(message: Message):
    await message.answer(
        text=LEXICON["nothing_to_cancel"], reply_markup=registration_inline_kb
    )


@router.message(Command(commands="cancel"), ~StateFilter(default_state))
@router.message(F.text == LEXICON["cancel_button"], ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext):
    await message.answer(text=LEXICON["cancel"], reply_markup=main_kb)
    await state.clear()


@router.message(StateFilter(FSMRegistration.fill_name), F.text.isalpha())
async def process_name_sent(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await message.answer(text=LEXICON["enter_age"], reply_markup=cancel_kb)
    await state.set_state(FSMRegistration.fill_age)


@router.message(StateFilter(FSMRegistration.fill_name))
async def incorrect_name(message: Message):
    await message.answer(text=LEXICON["incorrect_name"], reply_markup=cancel_kb)


@router.message(
    StateFilter(FSMRegistration.fill_age),
    lambda x: x.text.isdigit() and 1 <= int(x.text) <= 100,
)
async def process_age_sent(message: Message, state: FSMContext):
    await state.update_data(age=message.text)
    await message.answer(text=LEXICON["enter_sex"], reply_markup=sex_inline_kb)
    await state.set_state(FSMRegistration.fill_gender)


@router.message(StateFilter(FSMRegistration.fill_age))
async def incorrect_age(message: Message):
    await message.answer(text=LEXICON["incorrect_age"], reply_markup=cancel_kb)


@router.callback_query(
    StateFilter(FSMRegistration.fill_gender), F.data.in_(["male", "female"])
)
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)
    await callback.message.delete()
    await callback.message.answer(text=LEXICON["enter_descr"], reply_markup=cancel_kb)
    await state.set_state(FSMRegistration.fill_description)


@router.message(StateFilter(FSMRegistration.fill_gender))
async def incorrect_gender(message: Message):
    await message.answer(text=LEXICON["incorrect_gender"], reply_markup=cancel_kb)


@router.message(
    StateFilter(FSMRegistration.fill_description), lambda x: 1 <= len(x.text) <= 250
)
async def process_descr_sent(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(text=LEXICON["send_photo"], reply_markup=cancel_kb)
    await state.set_state(FSMRegistration.upload_photo)


@router.message(StateFilter(FSMRegistration.fill_description))
async def incorrect_descr(message: Message):
    await message.answer(text=LEXICON["incorrect_descr"], reply_markup=cancel_kb)


@router.message(
    StateFilter(FSMRegistration.upload_photo), F.photo[-1].as_("largest_photo")
)
async def process_photo_sent(
    message: Message, state: FSMContext, largest_photo: PhotoSize, database
):
    await state.update_data(
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id,
    )

    username = message.from_user.username
    user_id = message.from_user.id

    user_data = await state.get_data()

    if not database.get_profile(user_id):
        database.insert_user(user_data, user_id, username)
    else:
        database.update_user(user_id, username, user_data)

    await state.clear()
    await message.answer_sticker(LEXICON["form_completed_sticker"])
    await message.answer(text=LEXICON["form_completed"], reply_markup=main_kb)


@router.message(StateFilter(FSMRegistration.upload_photo))
async def incorrect_photo(message: Message):
    await message.answer(text=LEXICON["incorrect_photo"], reply_markup=cancel_kb)


@router.message(Command(commands="profile"), StateFilter(default_state))
@router.message(F.text == LEXICON["profile_button"], StateFilter(default_state))
async def show_profile(message: Message, database):
    user_id = message.from_user.id
    await show_user_profile(message, user_id, database)
