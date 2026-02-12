from datetime import datetime
import os
from aiogram import Router, F, Bot
from aiogram.enums import ChatType
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from db.crud.groups import get_groups
from db.crud.message import add_message
from db.crud.stopwords import get_stop_words
from db.crud.user import get_user, add_user, reduce_ad
from handlers.config import tg_id_list

error_chat = os.getenv('ERROR_CHAT_ID')

router = Router()

@router.message(F.chat.type.in_({ChatType.GROUP, ChatType.SUPERGROUP}))
async def check_pay(message: Message, bot: Bot):

    available_groups = await get_groups()

    # group_ids = [group.group_id for group in available_groups]

    chat_id = message.chat.id

    tg_id = message.from_user.id

    try:

        stopwords = await get_stop_words()

        for stopword in stopwords:
            if message.text or message.caption:
                if stopword.word in message.text if message.text else message.caption:
                    await bot.delete_message(chat_id, message.message_id)

                    return

        if tg_id in tg_id_list:
            if message.text.startswith('/'):
                await bot.delete_message(chat_id=chat_id, message_id=message.message_id)
            return





        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='✅ Получить доступ', url='https://t.me/Lavanda_helpbot?start')
                ]
            ]
        )

        # if chat_id in group_ids:


        user = await get_user(tg_id)

        if user:
            if user.ads_limit >= 1:

                await reduce_ad(tg_id)

            else:



                msg_id = message.message_id
                await bot.delete_message(chat_id=chat_id, message_id=msg_id)
                bot_msg_id = await message.answer(text=f'{message.from_user.first_name}, пока вы не можете отправлять сообщения в этом чате. Перейдите в @Lavanda_helpbot и получите доступ к чату.', reply_markup=keyboard)

                await add_message(bot_msg_id.message_id, 'user_block', datetime.utcnow(), chat_id)



        else:
            msg_id = message.message_id
            await bot.delete_message(chat_id=chat_id, message_id=msg_id)
            bot_msg_id = await message.answer(
                text=f'{message.from_user.first_name}, пока вы не можете отправлять сообщения в этом чате. Перейдите в @Lavanda_helpbot и получите доступ к чату.', reply_markup=keyboard)

            await add_message(bot_msg_id.message_id, 'user_block', datetime.utcnow(), chat_id)

            await add_user(tg_id, message.from_user.username)
    except TelegramBadRequest as e:

        await bot.send_message(chat_id=error_chat, text=f'Ошибка при удалении сообщения: {e}')

    except Exception as e:

        await bot.send_message(chat_id=error_chat, text=f'Произошла ошибка: {e}')