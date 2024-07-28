from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, F, Router
from aiogram import Dispatcher
import logging
import asyncio

from aiogram.utils.keyboard import ReplyKeyboardBuilder

from data.database import create_session
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from utils.keyboards import (passenger_kb, start_kb, order_kb,
                             choose_passengers, choose_point_kb, choose_address_kb,
                             choose_price, points, go_home_passenger)
from sqlalchemy import select
from data.user_form import User
from utils.forms import Form
from data.stats_class import Stats

passenger_router = Router(name=__name__)


@passenger_router.callback_query(F.data == 'home')
async def home(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text(text='Добро пожаловать в бота!', reply_markup=start_kb())


@passenger_router.callback_query(F.data == 'passenger')
async def start_function(query: CallbackQuery, state: FSMContext):
    session = await create_session()
    user = await session.execute(select(User).filter_by(user_id=str(query.message.chat.id)))
    user = user.scalars().first()
    user.who = 'passenger'
    await session.commit()
    await session.close()
    await query.message.edit_text('Выберите действие:', reply_markup=passenger_kb())


@passenger_router.callback_query(F.data == 'support')
async def start_function(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text('Поддержка: @kotikotikotikotiki', reply_markup=go_home_passenger())


@passenger_router.callback_query(F.data == 'end_trip')
@passenger_router.callback_query(F.data == 'cancel_trip')
async def end_trip(query: CallbackQuery, state: FSMContext):
    sess = await create_session()
    user = await sess.execute(select(User).filter_by(user_id=str(query.message.chat.id)))
    user = user.scalars().first()
    driver = await sess.execute(select(User).filter_by(user_id=str(user.my_drivers_id)))
    driver = driver.scalars().first()
    driver.passengers_left += user.passengers
    if not driver.my_passengers_ids.count(' '):
        driver.my_passengers_ids = ''
    else:
        driver.my_passengers_ids = driver.my_passengers_ids.replace(f' {user.user_id}', '')
    passengers_func = user.passengers
    price_func = 1
    user.point, user.address_from, user.address_to, user.passengers, user.price, user.my_drivers_id = None, None, None, None, None, None
    user.active = False
    if 'end_trip' == query.data:
        Stats.day += 1
        Stats.month += 1
        Stats.all += 1
        await query.message.edit_text('Выберите действие:', reply_markup=passenger_kb())
    else:
        await query.message.bot.send_message(chat_id=driver.user_id, text='Ваш заказ отменен')
        driver.driver_balance += price_func * passengers_func
        await query.message.edit_text('Выберите действие:', reply_markup=passenger_kb())

    await sess.commit()
    await sess.close()
    await state.clear()


@passenger_router.callback_query(F.data == 'order')
async def order(query: CallbackQuery, state: FSMContext):
    await query.message.answer(text='Выберите населенный пункт',
                               reply_markup=choose_point_kb())
    await state.set_state(Form.point)


@passenger_router.message(Form.point)
async def point(msg: Message, state: FSMContext):
    session = await create_session()
    user = await session.execute(select(User).
                                 filter_by(user_id=str(msg.from_user.id)))
    user = user.scalars().first()
    try:
        text = msg.text
        if text not in points:
            await msg.answer('Некорректный пункт')
            await state.set_state(Form.point)
        else:
            user.point = text
            await msg.answer('Введите адрес прибытия или выберите из недавних:\n'
                             f'1 - {user.last_1_address_to if user.last_1_address_to else "Недоступно"}\n'
                             f'2 - {user.last_2_address_to if user.last_2_address_to else "Недоступно"}\n'
                             f'3 - {user.last_3_address_to if user.last_3_address_to else "Недоступно"}'
                             , reply_markup=choose_address_kb())
            await session.commit()
            await state.set_state(Form.address_to)

    except Exception as err:
        await msg.answer('Выберите населенный пункт из списка',
                         reply_markup=choose_point_kb())
        await state.set_state(Form.point)
    await session.close()


@passenger_router.message(Form.address_to)
async def address_to(msg: Message, state: FSMContext):
    session = await create_session()
    user = await session.execute(select(User).
                                 filter_by(user_id=str(msg.from_user.id)))
    user = user.scalars().first()
    try:
        text = msg.text
        if text not in '123' and len(text) < 3:
            raise Exception
        if text == '1':
            if user.last_1_address_to:
                user.address_to = user.last_1_address_to
            else:
                raise Exception

        elif text == '2':
            if user.last_2_address_to:
                user.address_to = user.last_2_address_to
            else:
                raise Exception

        elif text == '3':
            if user.last_3_address_to:
                user.address_to = user.last_3_address_to
            else:
                raise Exception
        else:
            user.address_to = msg.text

        user.last_3_address_to = user.last_2_address_to
        user.last_2_address_to = user.last_1_address_to
        user.last_1_address_to = user.address_to

        await msg.answer('Введите адрес оправления или выберите из недавних:\n'
                         f'1 - {user.last_1_address_from if user.last_1_address_from else "Недоступно"}\n'
                         f'2 - {user.last_2_address_from if user.last_2_address_from else "Недоступно"}\n'
                         f'3 - {user.last_3_address_from if user.last_3_address_from else "Недоступно"}\n'
                         , reply_markup=choose_address_kb())
        await session.commit()
        await state.set_state(Form.address_from)
    except Exception as err:
        print(err)
        await msg.answer('Введите адрес прибытия или выберите из недавних:\n'
                         f'1 - {user.last_1_address_to if user.last_1_address_to else "Недоступно"}\n'
                         f'2 - {user.last_2_address_to if user.last_2_address_to else "Недоступно"}\n'
                         f'3 - {user.last_3_address_to if user.last_3_address_to else "Недоступно"}'
                         , reply_markup=choose_address_kb())
        await state.set_state(Form.address_to)

    finally:
        await session.close()


@passenger_router.message(Form.address_from)
async def address_from(msg: Message, state: FSMContext):
    session = await create_session()
    user = await session.execute(select(User).
                                 filter_by(user_id=str(msg.from_user.id)))
    user = user.scalars().first()
    try:
        text = msg.text
        if text not in '123' and len(text) < 3:
            raise Exception
        if text == '1':
            if user.last_1_address_from:
                user.address_from = user.last_1_address_from
            else:
                raise Exception
        elif text == '2':
            if user.last_2_address_from:
                user.address_from = user.last_2_address_from
            else:
                raise Exception
        elif text == '3':
            if user.last_3_address_from:
                user.address_from = user.last_3_address_from
            else:
                raise Exception
        else:
            user.address_from = msg.text
        user.last_3_address_from = user.last_2_address_from
        user.last_2_address_from = user.last_1_address_from
        user.last_1_address_from = user.address_from
        await msg.answer('Введите количество пассажиров(максимум 4)'
                         , reply_markup=choose_passengers())
        await session.commit()
        await state.set_state(Form.passengers)
    except Exception as err:
        print(err)
        await msg.answer('Введите адрес оправления или выберите из недавних:\n'
                         f'1 - {user.last_1_address_from if user.last_1_address_from else "Недоступно"}\n'
                         f'2 - {user.last_2_address_from if user.last_2_address_from else "Недоступно"}\n'
                         f'3 - {user.last_3_address_from if user.last_3_address_from else "Недоступно"}\n'
                         , reply_markup=choose_address_kb())
        await state.set_state(Form.address_from)

    finally:
        await session.close()


@passenger_router.message(Form.passengers)
async def passengers(msg: Message, state: FSMContext):
    session = await create_session()
    user = await session.execute(select(User).
                                 filter_by(user_id=str(msg.from_user.id)))
    user = user.scalars().first()
    try:
        text = int(msg.text)
        if not 0 < text < 5:
            raise Exception
        user.passengers = text
        await msg.answer('Введите стоимость поездки:', reply_markup=choose_price())
        await session.commit()
        await state.set_state(Form.price)
    except Exception as err:
        await msg.answer('Введите количество пассажиров(максимум 4)',
                         reply_markup=choose_passengers())
        await state.set_state(Form.passengers)

    finally:
        await session.close()


from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

@passenger_router.message(Form.price)
async def price(msg: Message, state: FSMContext):
    session = await create_session()
    user = await session.execute(select(User).
                                 filter_by(user_id=str(msg.from_user.id)))
    user = user.scalars().first()
    try:
        text = int(msg.text)
        if not 0 < text < 10000:
            raise Exception
        user.price = text
        user.active = True
        await msg.answer('Ваш заказ создан!\n'
                         'Когда водитель примет ваш заказ, вам придет уведомление')

        message_to_group = await msg.bot.send_message(chat_id=-1002249861834, text=f'Новый заказ!\n'
                                                                f'Заказчик: {msg.from_user.full_name}\n'
                                                                f'Район: {user.point}\n'
                                                                f'Откуда: {user.address_from}\n'
                                                                f'Куда: {user.address_to}\n'
                                                                f'Количество пассажиров: {user.passengers}\n'
                                                                f'Стоимость: {user.price}\n')
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Взять заказ', callback_data=f'take_an_order:{user.user_id}:{message_to_group.message_id}')]
        ])
        await msg.bot.edit_message_reply_markup(chat_id=-1002249861834, message_id=message_to_group.message_id
                                                , reply_markup=markup)
        await session.commit()
        await state.clear()


    except Exception as err:
        await msg.answer('Введите стоимость поездки:',
                         reply_markup=choose_price())
        await state.set_state(Form.price)
    finally:
        await session.close()
