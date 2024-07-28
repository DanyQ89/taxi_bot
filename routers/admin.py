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
from utils.keyboards import (go_home_main, admin_kb, go_home_driver, go_home_admin)
from sqlalchemy import select
from data.user_form import User
from utils.forms import Form
from data.stats_class import Stats

admin_router = Router(name=__name__)


@admin_router.callback_query(F.data == 'admin')
async def admin_password(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text('Введите пароль:', reply_markup=go_home_main())
    await state.set_state(Form.password)


@admin_router.message(Form.password)
async def admin(msg: Message, state: FSMContext):
    try:
        text = msg.text
        if text != 'Darxan2023+':
            await msg.answer('Некорректный пароль', reply_markup=go_home_main())
        else:
            sess = await create_session()
            user = await sess.execute(select(User).filter_by(user_id=str(msg.from_user.id)))
            user = user.scalars().first()
            user.who = 'admin'
            await sess.commit()
            await sess.close()
            await msg.answer('Выберите действие:', reply_markup=admin_kb())
    except Exception as err:
        await msg.message.edit_text('Введите пароль:', reply_markup=go_home_main())
        await state.set_state(Form.password)

@admin_router.callback_query(F.data == 'admin_passed')
async def admin_passed(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text('Выберите действие:', reply_markup=admin_kb())

@admin_router.callback_query(F.data == 'stats')
async def stats(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text('Ваша статистика заказов:\n'
                                  f'День: {Stats.day}\n'
                                  f'Месяц: {Stats.month}\n'
                                  f'За все время: {Stats.all}\n', reply_markup=go_home_admin())

@admin_router.callback_query(F.data == 'change_balance_driver')
async def change_balance_driver(query: CallbackQuery, state: FSMContext):
    await query.message.edit_text('Введите каждый параметр на новой строке:\n'
                                  'ник водителя в формате @123\n'
                                  'операцию в формате +/-\n'
                                  'сумму денег\n'
                                  'Пример:\n'
                                  '@123\n'
                                  '+\n'
                                  '1000', reply_markup=go_home_admin())

    await state.set_state(Form.change_balance_driver)


@admin_router.callback_query(Form.change_balance_driver)
async def change_balance(msg: Message, state: FSMContext):
    try:
        text = msg.text
        username, operation, amount = text.split('\n')
        if username and operation and amount:
            sess = await create_session()
            user = await sess.execute(select(User).filter_by(username=username[1:]))
            user = user.scalars().first()
            if operation == '+':
                user.driver_balance += int(amount)
            elif operation == '-':
                user.driver_balance -= int(amount)
            await sess.commit()
            await sess.close()
            await msg.message.edit_text('Операция успешно выполнена!', reply_markup=go_home_admin())
        else:
            raise Exception
    except Exception as err:
        await msg.message.edit_text('Введите каждый параметр на новой строке:\n'
                                    'ник водителя в формате @123\n'
                                    'операцию в формате +/-\n'
                                    'сумму денег\n'
                                    'Пример:\n'
                                    '@123\n'
                                    '+\n'
                                    '1000', reply_markup=go_home_driver())
        await state.set_state(Form.change_balance_driver)


@admin_router.callback_query(F.data == 'block_driver')
async def driver_delete(msg: Message, state: FSMContext):
    await msg.message.edit_text('Вы находитесь в режиме блокировки водителя.\n'
                                'Введите ник водителя в формате @123', reply_markup=go_home_admin())
    await state.set_state(Form.block_driver)

@admin_router.message(Form.block_driver)
async def driver_delete(msg: Message, state: FSMContext):
    try:
        username = msg.text
        if username:
            sess = await create_session()
            user = await sess.execute(select(User).filter_by(username=username[1:]))
            user = user.scalars().first()
            user.blocked = True
            await sess.commit()
            await sess.close()
            await msg.message.edit_text('Водитель успешно заблокирован!', reply_markup=go_home_admin())
        else:
            raise Exception
    except Exception as err:
        await msg.message.edit_text('Вы находитесь в режиме блокировки водителя.\n'
                                    'Введите ник водителя в формате @123', reply_markup=go_home_admin())
        await state.set_state(Form.block_driver)

@admin_router.callback_query(F.data == 'unblock_driver')
async def driver_delete(msg: Message, state: FSMContext):
    await msg.message.edit_text('Вы находитесь в режиме разблокировки водителя.\n'
                                'Введите ник водителя в формате @123', reply_markup=go_home_admin())
    await state.set_state(Form.unblock_driver)

@admin_router.message(Form.unblock_driver)
async def driver_delete(msg: Message, state: FSMContext):
    try:
        username = msg.text
        if username:
            sess = await create_session()
            user = await sess.execute(select(User).filter_by(username=username[1:]))
            user = user.scalars().first()
            user.blocked = False
            await sess.commit()
            await sess.close()
            await msg.message.edit_text('Водитель успешно разблокирован!', reply_markup=go_home_admin())
        else:
            raise Exception
    except Exception as err:
        await msg.message.edit_text('Вы находитесь в режиме разблокировки водителя.\n'
                                    'Введите ник водителя в формате @123', reply_markup=go_home_admin())
        await state.set_state(Form.unblock_driver)