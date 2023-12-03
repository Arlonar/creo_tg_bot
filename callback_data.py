from aiogram.filters.callback_data import CallbackData

class ChangeProfile(CallbackData, prefix="change_profile"):
    data_type: str
    test: bool
    