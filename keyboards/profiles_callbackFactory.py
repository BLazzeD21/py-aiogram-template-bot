from aiogram.filters.callback_data import CallbackData


class ProfilesCallbackFactory(CallbackData, prefix="profile"):
    user_id: str
    page_number: int

class ChangePageCallbackFactory(CallbackData, prefix="page"):
    page_number: int
    method_answer: bool
