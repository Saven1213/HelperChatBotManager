import asyncio
import logging

from aiogram.client.default import DefaultBotProperties


from aiogram import Bot, Dispatcher

import os
import sys
from dotenv import load_dotenv

from db.database import create_db
from handlers.personal_bot import router as bot_router

load_dotenv()

TOKEN = str(os.getenv("BOT_TOKEN"))






bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode='html')
)

dp = Dispatcher()


async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    dp.include_router(bot_router)
    # await create_db()

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

        await asyncio.sleep(0.1)










if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
