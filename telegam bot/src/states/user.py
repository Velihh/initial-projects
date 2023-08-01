from aiogram.filters.state import StatesGroup, State

class UserStates(StatesGroup):
    charge = State()
    purpose = State()
    resources = State()
    item = State()
    purpose1 = State()
    resources1 = State()
    question = State()
    zag = State()

class regist(StatesGroup):
    playerFullName = State()
    character = State()
    tradition = State()
    confirmation = State()
