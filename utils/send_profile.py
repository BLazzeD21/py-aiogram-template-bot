from aiogram.types import Message, InlineKeyboardMarkup
from lexicon import LEXICON

async def send_profile(
    message: Message, user_data: tuple, keyboard: InlineKeyboardMarkup
) -> None:
    caption: str = LEXICON["get_profile_data"].format(
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