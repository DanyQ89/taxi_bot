from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from data.database import create_session

def start_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Пассажир', callback_data='passenger')
    builder.button(text='Водитель', callback_data='driver')
    builder.button(text='Админ', callback_data='admin')
    builder.adjust(1)
    return builder.as_markup()


def passenger_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Заказать такси', callback_data='order')
    builder.button(text='Тех. Поддержка', callback_data='support')
    builder.button(text='Назад', callback_data='home')
    builder.adjust(1)
    return builder.as_markup()

def driver_main_kb():
    builder = InlineKeyboardBuilder()
    # builder.button(text='Взять заказ', callback_data='take_an_order')
    builder.button(text='Тех. Поддержка', callback_data='support_driver')
    builder.button(text='Пополнить баланс', callback_data='balance')
    builder.button(text='Назад', callback_data='home')
    builder.adjust(1)
    return builder.as_markup()
def admin_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Статистика', callback_data='stats')
    builder.button(text='Зачислить/Снять средства водителю', callback_data='change_balance_driver')
    builder.button(text='Заблокировать водителя', callback_data='block_driver')
    builder.button(text='Разблокировать водителя', callback_data='unblock_driver')
    builder.button(text='Назад', callback_data='home')
    builder.adjust(1)
    return builder.as_markup()


def order_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Заказать такси', callback_data='order')
    builder.button(text='Назад', callback_data='passenger')
    builder.adjust(1)
    return builder.as_markup()


points = 'Батыр, Мангышлак, Актау, Кызылтобе, Кызылтобе-2, Дача, Автодром'.split(', ')


def choose_point_kb():
    builder = ReplyKeyboardBuilder()
    for point in points:
        builder.button(text=point)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def choose_address_kb():

    builder = ReplyKeyboardBuilder()
    for i in '123':
        if i:
            builder.button(text=i)

    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def choose_passengers():
    builder = ReplyKeyboardBuilder()
    for passenger in ['1', '2', '3', '4']:
        builder.button(text=passenger)
    builder.adjust(4)
    return builder.as_markup(resize_keyboard=True)


prices = [350, 400, 450, 500, 550, 600, 700, 800, 1000, 1500, 2000, 5000, 6000, 8000, 10000]
def choose_price():
    builder = ReplyKeyboardBuilder()
    for price in [str(i) for i in prices]:
        builder.button(text=price)
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)


def go_home_passenger():
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад', callback_data='passenger')
    return builder.as_markup()


def go_home_driver():
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад', callback_data='driver')
    return builder.as_markup()

def go_home_admin():
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад', callback_data='admin_passed')
    return builder.as_markup()

def go_home_main():
    builder = InlineKeyboardBuilder()
    builder.button(text='Назад', callback_data='home')
    return builder.as_markup()


def contact_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Отправить контакт', request_contact=True)
    builder.adjust(1)
    return builder.as_markup(resize_keyboard=True)

def describe_car_kb():
    builder = ReplyKeyboardBuilder()
    builder.button(text='Не планирую быть водителем')
    return builder.as_markup(resize_keyboard=True)

def end_trip_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Завершить поездку', callback_data='end_trip')
    builder.button(text='Отменить поездку', callback_data='cancel_trip')
    return builder.as_markup()

def go_or_cancel():
    builder = InlineKeyboardBuilder()
    builder.button(text='Я еду', callback_data='order_has_taken')
    builder.button(text='Отмена', callback_data='order_has_canceled')
    return builder.as_markup()

def just_end_trip_kb():
    builder = InlineKeyboardBuilder()
    builder.button(text='Завершить поездку', callback_data='end_trip')
    builder.button(text='Назад', callback_data='driver')
    return builder.as_markup()