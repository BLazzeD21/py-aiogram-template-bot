from utils import send_profile
from aiogram.types import Message
from models.methods import DatabaseMethods
from lexicon import LEXICON
from keyboards.reply_keyboards import main_kb
from keyboards.inline_keyboards import registration_inline_kb, settings_inline_kb

async def show_user_profile(
    message: Message, user_id: int, database: DatabaseMethods
) -> None:
    try:
        await database.connect()
        user_data: tuple = await database.get_profile(user_id)

        if user_data:
            await send_profile(message, user_data, settings_inline_kb)
        else:
            await message.answer(
                text=LEXICON["not_registered"], reply_markup=registration_inline_kb
            )
    except:
        await message.answer(text=LEXICON["db_error"], reply_markup=main_kb)
    finally:
        await database.close()