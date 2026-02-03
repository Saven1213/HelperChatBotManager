from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from db.crud.groups import get_groups
from db.crud.message import get_messages




async def push_ad(bot: Bot):

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
            [InlineKeyboardButton(text="🔑 Доступ", url="https://t.me/Lavanda_helpbotbot"),
            InlineKeyboardButton(text="💬 Сеть чатов", callback_data="chat_network_info")],
            [InlineKeyboardButton(text="📢 Реклама", url="https://t.me/Lavanda_ads_bot"),
            InlineKeyboardButton(text="❓ FAQ", url="https://t.me/")]
        ]
    )

    for group in groups:
        await bot.send_photo(
            chat_id=group.group_id,
            photo='AgACAgIAAxkBAAOQaYJLVZCDQ3kGKE7KahN435njRgYAAvYMaxvPsRlIs87OpGTmozABAAMCAAN5AAM4BA',
            caption=text,
            reply_markup=keyboard
        )


