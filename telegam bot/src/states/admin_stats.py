from aiogram.filters.state import StatesGroup, State

class AdminStates(StatesGroup):
    find_user = State()
    find_dis = State()
    name_dis = State()
    geo = State()
    radius = State()
    add_dis = State()
    new_name = State()
    new_name1 = State()
    timer = State()
    anomaly = State()
    charge_dis = State()
    zag = State()