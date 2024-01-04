from utils import send_profile
from aiogram.types import CallbackQuery, InlineKeyboardMarkup
from models.methods import DatabaseMethods
from lexicon import LEXICON
from keyboards.reply_keyboards import main_kb
from keyboards.create_inline_kb import create_back_to_page

async def show_another_users_profile(
    callback: CallbackQuery, user_id: int, database: DatabaseMethods, page: int
) -> None:
    try:
        await database.connect()
        user_data: tuple = await database.get_profile(user_id)

        keyboard: InlineKeyboardMarkup = create_back_to_page(page)

        if user_data:
            await callback.message.delete()
            await send_profile(callback.message, user_data, keyboard)
        else:
            await callback.answer(text=LEXICON["not_exist"])
    except:
        await callback.message.answer(text=LEXICON["db_error"], reply_markup=main_kb)
    finally:
        await database.close()