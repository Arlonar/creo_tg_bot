from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):
    profile_set_first_name = State()
    profile_set_last_name = State()
    profile_set_gender = State()
    profile_set_email = State()
    profile_set_address = State()
    profile_set_phone = State()

    order_set_title = State()
    order_set_description = State()
    order_set_amount = State()
    