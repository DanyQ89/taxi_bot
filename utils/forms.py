from aiogram.fsm.state import State, StatesGroup

class Form(StatesGroup):
    who = State()
    point = State()
    address_to = State()
    address_from = State()
    passengers = State()
    price = State()
    username = State()
    contact = State()
    car = State()
    password = State()
    change_balance_driver = State()
    block_driver = State()
    unblock_driver = State()