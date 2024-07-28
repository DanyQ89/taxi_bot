from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from utils.keyboards import start_kb, contact_kb, describe_car_kb
from utils.forms import Form
from data.database import create_session
from sqlalchemy import select
from data.user_form import User

start_router = Router(name=__name__)

@start_router.message(CommandStart())
async def start_function(message: Message, state: FSMContext):
    sess = await create_session()
    user = await sess.execute(select(User).filter_by(user_id=str(message.from_user.id)))
    user = user.scalars().first()
    if not user:
        user = User(user_id=str(message.from_user.id), username=message.from_user.username)
        sess.add(user)
        await sess.commit()
        await message.answer('Отправьте свой мобильный номер', reply_markup=contact_kb())
        await state.set_state(Form.contact)
    else:
        user.username = message.from_user.username
        await sess.commit()
        await message.answer('Добро пожаловать в бота!', reply_markup=start_kb())
    await sess.close()

@start_router.message(Form.contact)
async def contact_car(message: Message, state: FSMContext):
    sess = await create_session()
    user = await sess.execute(select(User).filter_by(user_id=str(message.from_user.id)))
    user = user.scalars().first()
    try:
        user.number = message.contact.phone_number
        await sess.commit()
        await message.answer('Если вы планируете быть водителем, опишите свою машину\n'
                             'Вам будет начислено 10000 рублей, они будут сниматься за каждого пассажира в размере 100 рублей/пассажир', reply_markup=describe_car_kb())
        await state.set_state(Form.car)
    except Exception as err:
        await message.answer('Отправьте свой мобильный номер', reply_markup=contact_kb())
        await state.set_state(Form.contact)
    finally:
        await sess.close()


@start_router.message(Form.car)
async def car_start(message: Message, state: FSMContext):
    sess = await create_session()
    user = await sess.execute(select(User).filter_by(user_id=str(message.from_user.id)))
    user = user.scalars().first()
    try:
        if message.text == 'Не планирую быть водителем':
            user.my_car = ''
        else:
            user.driver_balance = 10000
            user.my_car = message.text
        await sess.commit()
        await message.answer('Добро пожаловать в бота!', reply_markup=start_kb())
        await state.clear()
    except Exception as err:
        await message.answer('Если вы планируете быть водителем, опишите свою машину', reply_markup=describe_car_kb())
        await state.set_state(Form.car)
    finally:
        await sess.close()

