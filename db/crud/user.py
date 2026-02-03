
from sqlalchemy import select
from db.models import User

from db.database import async_session


async def get_user(tg_id: int):
    async with async_session() as session:
        result = await session.execute(select(User).where(User.tg_id == tg_id))
        user = result.scalar_one_or_none()

        return user

async def add_user(tg_id: int, username: str):
    async with async_session() as session:

        user = User(
            tg_id=tg_id,
            username=username,
            ads_limit=0
        )

        session.add(user)

        await session.commit()