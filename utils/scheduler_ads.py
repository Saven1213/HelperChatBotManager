import os

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputFile, FSInputFile

from db.crud.groups import get_groups
from db.crud.message import get_messages

from datetime import datetime
from zoneinfo import ZoneInfo




async def push_ad(bot: Bot):


    moscow_time = datetime.now(ZoneInfo("Europe/Moscow"))

    if 0 <= moscow_time.hour < 6:
        return

    groups = await get_groups()

    messages = await get_messages()

    if messages:
        for message in messages:
            if message.status == 'active' and message.type == 'ad':
                try:
                    await bot.delete_message(chat_id=message.chat_id, message_id=message.message_id)
                except TelegramBadRequest:
                    pass

    text = ('‼️ Внимание! Чтобы размещать объявления в чате получите доступ в боте 👉 @Lavanda_helpbot\n\n'
              '⚠️ Получая доступ в боте, вы соглашаетесь с пользовательским соглашением.\n'
              '➡️ Данный бот-доступа единый на всю сеть из 26 чатов Краснодарского края\n\n'
              '⏰ Время работы чата: с 8:00 до 23:00!\n\n'
              '🔥 Условия по рекламе тут 👉 @Lavanda_ads_bot\n\n'
            )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔑 Доступ", url="https://t.me/Lavanda_helpbot"),
            InlineKeyboardButton(text="📍 Сеть чатов", url='https://t.me/addlist/8fGeGpWoxMVkNWIy')],
            [InlineKeyboardButton(text="📢 Реклама", url="https://t.me/Lavanda_ads_bot"),
            InlineKeyboardButton(text="❓ FAQ", url="https://telegra.ph/FAQ-CHasto-zadavaemye-voprosy-02-04-2")]
        ]
    )


    current_file_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_file_dir)
    photos_dir = os.path.join(parent_dir, 'pictures')
    photo_path = os.path.join(photos_dir, 'main_info.jpg')

    photo = FSInputFile(photo_path)

    for group in groups:

        await bot.send_photo(
            chat_id=group.group_id,
            photo=photo,
            caption=text,
            reply_markup=keyboard
        )



