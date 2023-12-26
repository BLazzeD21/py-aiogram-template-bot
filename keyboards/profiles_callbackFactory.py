from aiogram.filters.callback_data import CallbackData


class ProfilesCallbackFactory(CallbackData, prefix="profile"):
    user_id: str
    page_number: str

class ChangePageCallbackFactory(CallbackData, prefix="page"):
    page_number: str
