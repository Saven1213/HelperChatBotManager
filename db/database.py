from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession

from db.config import settings
from db.models import Base

engine = create_async_engine(
    url=settings.db_url_asyncpg(),
    echo=True,

)

async_session = async_sessionmaker(bind=engine, class_=AsyncSession)

async def create_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


