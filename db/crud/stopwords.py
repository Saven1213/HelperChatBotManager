from sqlalchemy import select

from db.database import async_session
from db.models import StopWord


async def get_stop_words():
    async with async_session() as session:

        res = await session.execute(select(StopWord))

        stopwords = res.scalars().all()

        return stopwords

async def add_stop_words(stopwords):
    async with async_session() as session:
        if isinstance(stopwords, str):
            stopwords = [stopwords]

        for word in stopwords:
            sw = StopWord(word=word)
            session.add(sw)

        await session.commit()
