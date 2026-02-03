from datetime import datetime, timedelta

from aiogram import Bot

from db.crud.message import get_messages, mark_as_deleted


async def check_messages(bot: Bot):
    messages = await get_messages()

    if not messages:
        return

    now = datetime.utcnow()

    for message in messages:
        if message.type == 'user_block' and message.status == 'active':

            if now - message.time >= timedelta(seconds=20):
                try:
                    await bot.delete_message(
                        chat_id=message.chat_id,
                        message_id=message.message_id
                    )

                    await mark_as_deleted(message.id)
                    print(f"✅ Удалено сообщение {message.id}")
                except Exception as e:
                    print(f"❌ Не удалось удалить {message.id}: {e}")

                    await mark_as_deleted(message.id)
