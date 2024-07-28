from aiogram import Router
from .start import start_router
from .passenger import passenger_router
from .driver import driver_router
from .admin import admin_router

router = Router(name=__name__)

router.include_routers(start_router, passenger_router, driver_router, admin_router)