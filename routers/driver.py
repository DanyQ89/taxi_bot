from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, F, Router
from aiogram import Dispatcher
import logging
import asyncio

from aiogram.utils.keyboard import ReplyKeyboardBuilder

from data.database import create_session
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.context import FSMContext
from utils.keyboards import (passenger_kb, start_kb, order_kb,
                             choose_passengers, choose_point_kb, choose_address_kb,
                             choose_price, points, driver_main_kb, go_home_driver, end_trip_kb, go_home_main, go_home_passenger)
from sqlalchemy import select
from data.user_form import User
from utils.forms import Form
from data.stats_class import Stats

driver_router = Router(name=__name__)


@driver_router.callback_query(F.data == 'driver')
async def driver(query: CallbackQuery, state: FSMContext):
    sess = await create_session()
    user = await sess.execute(select(User).filter_by(user_id=str(query.message.chat.id)))
    user = user.scalars().first()
    user.who = 'driver'
    if not user.blocked:
        if not user.my_car:
            await query.message.edit_text('🚗 Опишите свою машину')
            await state.set_state(Form.car)
            await sess.close()
        else:
            await query.message.edit_text(text='👨‍💼 Выберите действие:', reply_markup=driver_main_kb())
            await sess.commit()
            await sess.close()
    else:
        await query.message.edit_text('🚫 Вы были заблокированы', reply_markup=go_home_main())


@driver_router.callback_query(F.data == 'support_driver')
async def support_driver(query: CallbackQuery):
    await query.message.edit_text('💬 Поддержка: @kotikotikotikotiki', reply_markup=go_home_driver())


@driver_router.callback_query(F.data == 'balance')
async def balance(query: CallbackQuery):
    session = await create_session()
    user = await session.execute(select(User).filter_by(user_id=str(query.message.chat.id)))
    user = user.scalars().first()
    if not user.blocked:
        await query.message.edit_text(f'💰 Ваш баланс: {user.driver_balance}\n'
                                      f'📝 Инструкции по пополнению баланса: @123',
                                      reply_markup=go_home_driver())
    else:
        await query.message.edit_text('🚫 Вы были заблокированы', reply_markup=go_home_main())




@driver_router.callback_query(F.data.startswith('take_an_order'))
async def take_an_order(query: CallbackQuery, state: FSMContext):
    user_id = query.data.split(':')[1]
    message_id = query.data.split(':')[2]
    session = await create_session()
    user_func = await session.execute(select(User).filter_by(user_id=user_id))
    user_func = user_func.scalars().first()
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🚗 Я еду', callback_data=f'order_has_taken:{user_id}:{message_id}')],
        [InlineKeyboardButton(text='❌ Отменить заказ', callback_data=f'order_has_canceled:{user_id}:{message_id}')]
    ])
    await query.message.bot.send_message(chat_id=user_id,
                                         text='✅ Ваш заказ принят, мы уведомим вас, когда водитель начнет выезжать')

    print(query.from_user.id)
    await query.message.bot.send_message(chat_id=query.from_user.id, text=f'👤 Заказчик: {user_func.number}\n'
    f'📍 Район: {user_func.point}\n'
    f'🏠 Откуда: {user_func.address_from}\n'
    f'🏢 Куда: {user_func.address_to}\n'
    f'👥 Количество пассажиров: {user_func.passengers}\n'
    f'💰 Стоимость: {user_func.price}\n')
    await query.message.bot.send_message(chat_id=query.from_user.id, text='📝 Выберите одну из двух кнопок',
                                         reply_markup=markup)
    await query.message.bot.delete_message(chat_id=-1002249861834,
                                           message_id=int(message_id))

from utils.keyboards import just_end_trip_kb
@driver_router.callback_query(F.data.startswith('order_has_taken'))
async def order_has_taken(query: CallbackQuery, state: FSMContext):
    user_id = query.data.split(':')[1]
    message_id = query.data.split(':')[2]
    session = await create_session()
    try:
        user_func = await session.execute(select(User).filter_by(user_id=user_id))
        user_func = user_func.scalars().first()
        driver_func = await session.execute(select(User).filter_by(user_id=str(query.message.chat.id)))
        driver_func = driver_func.scalars().first()
        if not driver_func.blocked:
            price = 1
            if user_func and driver_func:
                if user_func.active:
                    if not driver_func.my_passengers_ids:
                        driver_func.passengers_left = 4
                    if driver_func.passengers_left >= user_func.passengers:
                        if driver_func.driver_balance >= price * user_func.passengers:
                            user_func.active = False
                            driver_func.passengers_left -= user_func.passengers
                            user_func.my_drivers_id = driver_func.user_id
                            #
                            driver_func.driver_balance -= price * user_func.passengers
                            #
                            arr = driver_func.my_passengers_ids
                            if not arr:
                                arr = str(user_func.user_id)
                            else:
                                arr += f' {user_func.user_id}'
                            driver_func.my_passengers_ids = arr
                            await query.message.delete()
                            markup = InlineKeyboardMarkup(inline_keyboard=[
                                [InlineKeyboardButton(text='✅ Завершить заказ',
                                                      callback_data=f'driver_end_order:{user_func.user_id}')],
                                [InlineKeyboardButton(text='🔙 Назад', callback_data='driver')],
                            ])
                            await query.message.answer('🚗 Отлично, можете выезжать за пассажиром!',

                                                       reply_markup=markup)
                            await query.message.bot.send_message(chat_id=user_func.user_id, text=f'✅ Ваш заказ принят!\n'
                                                                                                 f'👤 Водитель: {driver_func.number}\n'
                                                                                                 f'🚗 Данные автомобиля '
                                                                                                 f'водителя: '
                                                                                                 f'{driver_func.my_car}',
                                                                 reply_markup=end_trip_kb())
                            markup = InlineKeyboardMarkup(inline_keyboard=[])

                            await session.commit()
                        else:
                            await query.message.answer('💰 Пополните баланс, чтобы взять заказ',
                                                       reply_markup=go_home_driver())
                            await order_has_canceled(query, state, user_id=user_id)
                    else:
                        await query.message.answer('❌ Количество пассажиров пользователя превышает ваши оставшиеся места',
                                                   reply_markup=go_home_driver())
                        await order_has_canceled(query, state, user_id=user_id)

                else:
                    await query.message.answer('❌ Заказ пользователя уже был взят', reply_markup=go_home_driver())
                    await order_has_canceled(query, state, user_id=user_id)

            else:
                await query.message.answer('❌ Пользователь не найден', reply_markup=go_home_driver())
                await order_has_canceled(query, state, user_id=user_id)

        else:
            await query.message.answer('🚫 Вы были заблокированы', reply_markup=go_home_main())
            await order_has_canceled(query, state, user_id=user_id)
    except Exception as err:
        print(err)
    finally:
        await session.close()

@driver_router.callback_query(F.data.startswith('driver_end_order'))
async def end_order(query: CallbackQuery, state: FSMContext):
    await state.clear()
    user_id = query.data.split(':')[1]
    session = await create_session()
    try:
        user_func = await session.execute(select(User).filter_by(user_id=user_id))
        user_func = user_func.scalars().first()
        user_func.my_drivers_id = ''
        user_func.active = 0
        driver_func = await session.execute(select(User).filter_by(user_id=str(query.message.chat.id)))
        driver_func = driver_func.scalars().first()
        driver_func.passengers_left += user_func.passengers
        if not driver_func.my_passengers_ids.count(' '):
            driver_func.my_passengers_ids = ''
        else:
            driver_func.my_passengers_ids = driver_func.my_passengers_ids.replace(f' {user_func.user_id}', '')
        await query.message.edit_text('✅ Вы завершили данный заказ',
                                      reply_markup=go_home_driver())
        await query.message.bot.send_message(chat_id=user_func.user_id, text='✅ Водитель завершил ваш заказ',
                                             reply_markup=go_home_passenger())
        Stats.day += 1
        Stats.month += 1
        Stats.all += 1
        await session.commit()
    except Exception as err:
        pass
    finally:
        await session.close()

@driver_router.callback_query(F.data.startswith('order_has_canceled'))
async def order_has_canceled(query: CallbackQuery, state: FSMContext, user_id=None):
    if not user_id:
        user_id = query.data.split(':')[1]
    session = await create_session()
    try:
        user_func = await session.execute(select(User).filter_by(user_id=str(user_id)))
        user_func = user_func.scalars().first()
        driver_func = await session.execute(select(User).filter_by(user_id=str(query.message.chat.id)))
        driver_func = driver_func.scalars().first()
        user_func.active = True
        user_func.my_drivers_id = ''

        await query.message.delete()
        await query.message.bot.send_message(chat_id=user_func.user_id,
                                             text='❌ Данный водитель отменил ваш заказ, ожидайте другого водителя')
        await query.message.answer('❌ Вы отменили данный заказ')

        msg = await query.message.bot.send_message(chat_id=-1002249861834, text=f'📢 Новый заказ!\n'
                                                                                f'👤 Заказчик: {query.message.from_user.full_name}\n'
                                                                                f'📍 Район: {user_func.point}\n'
                                                                                f'🏠 Откуда: {user_func.address_from}\n'
                                                                                f'🏢 Куда: {user_func.address_to}\n'
                                                                                f'👥 Количество пассажиров: {user_func.passengers}\n'
                                                                                f'💰 Стоимость: {user_func.price}\n')
        markup = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='🚗 Взять заказ',
                                  callback_data=f'take_an_order:{user_func.user_id}:{msg.message_id}')]
        ])
        await query.message.bot.edit_message_reply_markup(chat_id=-1002249861834, message_id=msg.message_id,
                                                          reply_markup=markup)
        await session.commit()
    except Exception as err:
        pass
    finally:
        await session.close()
