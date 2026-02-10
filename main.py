import asyncio
import logging
from datetime import datetime

from aiogram.client.default import DefaultBotProperties
from apscheduler.schedulers.asyncio import AsyncIOScheduler


from aiogram import Bot, Dispatcher

import os
import sys
from dotenv import load_dotenv

from db.database import create_db
from handlers.groups import check_pay
from handlers.personal_bot import router as bot_router
from handlers.groups import router as groups_router
from utils.scheduler_ads import push_ad
from utils.sheduler_for_delete_messages import check_messages

load_dotenv()

TOKEN = str(os.getenv("BOT_TOKEN"))

scheduler = AsyncIOScheduler(timezone='Europe/Moscow')



bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode='html')
)

dp = Dispatcher()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_router(bot_router)
    dp.include_router(groups_router)
    # await create_db()

    scheduler.add_job(check_messages, 'interval', seconds=10, args=[bot])
    scheduler.add_job(push_ad, 'interval', hours=1, args=[bot])

    scheduler.start()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()
        if scheduler.running:
            scheduler.shutdown()

        await asyncio.sleep(0.1)










if __name__ == '__main__':
    # logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
