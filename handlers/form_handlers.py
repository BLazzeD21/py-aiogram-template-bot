from aiogram.types import CallbackQuery, Message, PhotoSize
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram import Router, F

from keyboards.reply_keyboards import main_kb, cancel_kb
from keyboards.inline_keyboards import sex_inline_kb, back_inline_kb, registration_inline_kb
from lexicon import LEXICON
from states import FSMRegistration
from models import user_dict


router = Router()

# ------------------------- Functions -------------------------


async def show_user_profile(message: Message, user_id):
    if user_id in user_dict:
        user_data = LEXICON["get_profile_data"].format(
            user_id=user_id,
            username=user_dict[user_id]["username"],
            name=user_dict[user_id]["name"],
            age=user_dict[user_id]["age"],
            gender=user_dict[user_id]["gender"],
            description=user_dict[user_id]["description"]
        )

        await message.answer_photo(
            photo=user_dict[user_id]["photo_id"],
            caption=user_data,
            reply_markup=back_inline_kb,
        )
    else:
        await message.answer(text=LEXICON["not_registered"], reply_markup=registration_inline_kb)


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
    await message.answer(text=LEXICON["nothing_to_cancel"], reply_markup=main_kb)


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


@router.callback_query(StateFilter(FSMRegistration.fill_gender), F.data.in_(["male", "female"]))
async def process_gender_press(callback: CallbackQuery, state: FSMContext):
    await state.update_data(gender=callback.data)
    await callback.message.delete()
    await callback.message.answer(text=LEXICON["enter_descr"], reply_markup=cancel_kb)
    await state.set_state(FSMRegistration.fill_description)


@router.message(StateFilter(FSMRegistration.fill_gender))
async def incorrect_gender(message: Message):
    await message.answer(text=LEXICON["incorrect_gender"], reply_markup=cancel_kb)


@router.message(StateFilter(FSMRegistration.fill_description), lambda x: 1 <= len(x.text) <= 250)
async def process_descr_sent(message: Message, state: FSMContext):
    await state.update_data(description=message.text)
    await message.answer(text=LEXICON["send_photo"], reply_markup=cancel_kb)
    await state.set_state(FSMRegistration.upload_photo)


@router.message(StateFilter(FSMRegistration.fill_description))
async def incorrect_descr(message: Message):
    await message.answer(text=LEXICON["incorrect_descr"], reply_markup=cancel_kb)


@router.message(StateFilter(FSMRegistration.upload_photo), F.photo[-1].as_("largest_photo"))
async def process_photo_sent(message: Message, state: FSMContext, largest_photo: PhotoSize):
    await state.update_data(
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id,
    )

    username = message.from_user.username
    user_id = message.from_user.id
    user_dict[user_id] = await state.get_data()
    user_dict[user_id]["user_id"] = user_id
    user_dict[user_id]["username"] = username
    print(user_dict[user_id])

    await state.clear()
    await message.answer(text=LEXICON["form_completed"], reply_markup=main_kb)


@router.message(StateFilter(FSMRegistration.upload_photo))
async def incorrect_photo(message: Message):
    await message.answer(text=LEXICON["incorrect_photo"], reply_markup=cancel_kb)


@router.message(Command(commands="profile"), StateFilter(default_state))
@router.message(F.text == LEXICON["profile_button"], StateFilter(default_state))
async def show_profile(message: Message):
    user_id = message.from_user.id
    await show_user_profile(message, user_id)
