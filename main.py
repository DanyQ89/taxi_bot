from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot
from aiogram import Dispatcher
import logging
import asyncio
from routers.init import router
from data.database import init_models
from data.stats_class import Stats
token = '7326331029:AAESSXyZWCYr_nRhEEq_NTRQDImxSvh9CNY'

bot = Bot(token=token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

logging.basicConfig(level=logging.INFO)

async def update_day():
    await asyncio.sleep(24 * 60 * 60)
    print('woke up')
    Stats.day = 0

async def update_month():
    await asyncio.sleep(30 * 24 * 60 * 60)
    Stats.month = 0


async def main():
    await init_models()
    dp = Dispatcher()
    dp.include_router(router)
    await asyncio.gather(
        update_day(),
        update_month(),
        dp.start_polling(bot)
    )


if __name__ == '__main__':
    asyncio.run(main())