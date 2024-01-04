from aiogram.types import CallbackQuery, Message, PhotoSize
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram import Router, F
from models.methods import DatabaseMethods

from keyboards.inline_keyboards import sex_inline_kb, registration_inline_kb
from keyboards.reply_keyboards import main_kb, cancel_kb
from lexicon import LEXICON
from states import FSMRegistration

router: Router = Router()


@router.callback_query(F.data == "form_button", StateFilter(default_state))
async def process_form_button_press(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()

    await callback.message.answer(text=LEXICON["enter_name"], reply_markup=cancel_kb)
    await state.set_state(FSMRegistration.fill_name)

    await callback.answer()


@router.message(F.text == LEXICON["cancel_button"], StateFilter(default_state))
async def process_cancel_command(message: Message) -> None:
    await message.answer(
        text=LEXICON["nothing_to_cancel"], reply_markup=registration_inline_kb
    )


@router.message(F.text == LEXICON["cancel_button"], ~StateFilter(default_state))
async def process_cancel_command_state(message: Message, state: FSMContext) -> None:
    await message.answer(text=LEXICON["cancel"], reply_markup=main_kb)
    await state.clear()


@router.message(StateFilter(FSMRegistration.fill_name), F.content_type.in_({"text"}))
async def process_name_sent(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.answer(text=LEXICON["enter_age"], reply_markup=cancel_kb)
    await state.set_state(FSMRegistration.fill_age)


@router.message(StateFilter(FSMRegistration.fill_name))
async def incorrect_name(message: Message) -> None:
    await message.answer(text=LEXICON["incorrect_name"], reply_markup=cancel_kb)


@router.message(
    StateFilter(FSMRegistration.fill_age),
    lambda x: x.text.isdigit() and 1 <= int(x.text) <= 100,
)
async def process_age_sent(message: Message, state: FSMContext) -> None:
    await state.update_data(age=message.text)
    await message.answer(text=LEXICON["enter_sex"], reply_markup=sex_inline_kb)
    await state.set_state(FSMRegistration.fill_gender)


@router.message(StateFilter(FSMRegistration.fill_age))
async def incorrect_age(message: Message) -> None:
    await message.answer(text=LEXICON["incorrect_age"], reply_markup=cancel_kb)


@router.callback_query(
    StateFilter(FSMRegistration.fill_gender), F.data.in_(["male", "female"])
)
async def process_gender_press(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(gender=callback.data)
    await callback.message.delete()
    await callback.message.answer(text=LEXICON["enter_descr"], reply_markup=cancel_kb)
    await state.set_state(FSMRegistration.fill_description)


@router.message(StateFilter(FSMRegistration.fill_gender))
async def incorrect_gender(message: Message) -> None:
    await message.answer(text=LEXICON["incorrect_gender"], reply_markup=cancel_kb)


@router.message(
    StateFilter(FSMRegistration.fill_description),
    F.content_type.in_({"text"}),
    lambda x: 1 <= len(x.text) <= 250,
)
async def process_descr_sent(message: Message, state: FSMContext) -> None:
    await state.update_data(description=message.text)
    await message.answer(text=LEXICON["send_photo"], reply_markup=cancel_kb)
    await state.set_state(FSMRegistration.upload_photo)


@router.message(StateFilter(FSMRegistration.fill_description))
async def incorrect_descr(message: Message) -> None:
    await message.answer(text=LEXICON["incorrect_descr"], reply_markup=cancel_kb)


@router.message(
    StateFilter(FSMRegistration.upload_photo), F.photo[-1].as_("largest_photo")
)
async def process_photo_sent(
    message: Message,
    state: FSMContext,
    largest_photo: PhotoSize,
    database: DatabaseMethods,
) -> None:
    await state.update_data(
        photo_unique_id=largest_photo.file_unique_id,
        photo_id=largest_photo.file_id,
    )

    username: str = message.from_user.username
    user_id: int = message.from_user.id

    user_data: tuple = await state.get_data()

    try:
        await database.connect()
        user: tuple = await database.get_profile(user_id)

        if not user:
            await database.insert_user(user_data, user_id, username)
        else:
            await database.update_user(user_id, username, user_data)

        await state.clear()

        await message.answer_sticker(
            LEXICON["form_completed_sticker"], reply_markup=main_kb
        )
        await message.answer(text=LEXICON["form_completed"])
    except:
        await message.answer(text=LEXICON["db_error"], reply_markup=main_kb)
    finally:
        await database.close()


@router.message(StateFilter(FSMRegistration.upload_photo))
async def incorrect_photo(message: Message) -> None:
    await message.answer(text=LEXICON["incorrect_photo"], reply_markup=cancel_kb)
