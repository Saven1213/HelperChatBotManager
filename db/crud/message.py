from sqlalchemy import select

from db.database import async_session
from db.models import Message


async def add_message(message_id, type_, time, chat_id):
    async with async_session() as session:
        message = Message(
            message_id=message_id,
            type=type_,
            time=time,
            chat_id=chat_id,
            status='active'
        )

        session.add(message)
        await session.commit()

async def get_messages():
    async with async_session() as session:
        res = await session.execute(select(Message))

        messages = res.scalars().all()

        return messages

async def mark_as_deleted(id_):
    async with async_session() as session:
        res = await session.execute(select(Message).where(Message.id == id_))

        message = res.scalar_one_or_none()

        if message:
            message.status = 'deleted'
            await session.commit()

