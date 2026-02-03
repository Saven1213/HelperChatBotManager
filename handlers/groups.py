from datetime import datetime

from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio
from db.crud.groups import get_groups
from db.crud.message import add_message
from db.crud.user import get_user, add_user

router = Router()

@router.message()
async def check_pay(message: Message, bot: Bot):

    available_groups = await get_groups()

    group_ids = [group.group_id for group in available_groups]

    chat_id = message.chat.id

    if chat_id in group_ids:
        tg_id = message.from_user.id

        user = await get_user(tg_id)

        if user:
            if user.ads_limit >= 1:
                return
            else:



                msg_id = message.message_id
                await bot.delete_message(chat_id=chat_id, message_id=msg_id)
                bot_msg_id = await message.answer(text=f'{message.from_user.first_name}, пока вы не можете отправлять сообщения в этом чате. Перейдите в @Lavanda_helpbot и получите доступ к чату.')

                await add_message(bot_msg_id, 'user_block', datetime.utcnow(), chat_id)



        else:
            msg_id = message.message_id
            await bot.delete_message(chat_id=chat_id, message_id=msg_id)
            bot_msg_id = await message.answer(
                text=f'{message.from_user.first_name}, пока вы не можете отправлять сообщения в этом чате. Перейдите в @Lavanda_helpbot и получите доступ к чату.')

            await add_message(bot_msg_id, 'user_block', datetime.utcnow(), chat_id)

            await add_user(tg_id, message.from_user.username)


