from .database import SqlAlchemyBase
from sqlalchemy import Column, String, LargeBinary, Float, Boolean, Integer
from sqlalchemy import Date


class User(SqlAlchemyBase):
    __tablename__ = 'users'

    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(String, unique=True, index=True)
    username = Column(String, unique=True)
    number = Column(String, unique=True)
    who = Column(String)
    point = Column(String)
    address_to = Column(String)
    address_from = Column(String)
    passengers = Column(Integer)
    price = Column(Integer)
    last_1_address_to = Column(String)
    last_2_address_to = Column(String)
    last_3_address_to = Column(String)
    last_1_address_from = Column(String)
    last_2_address_from = Column(String)
    last_3_address_from = Column(String)
    passengers_left = Column(String)
    my_drivers_id = Column(String)
    my_passengers_ids = Column(String)
    active = Column(Boolean)
    my_car = Column(String)
    driver_balance = Column(Integer, default=100)
    blocked = Column(Boolean, default=False)