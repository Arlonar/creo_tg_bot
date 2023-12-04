from aiogram.fsm.state import StatesGroup, State

class Gen(StatesGroup):
    set_first_name = State()
    set_last_name = State()
    set_gender = State()
    set_email = State()
    set_address = State()
    set_phone = State()

    change_profile = State()
    register_contractor = State()