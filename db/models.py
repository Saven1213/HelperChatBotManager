from typing import Optional

from sqlalchemy import String, Integer, Boolean, Float, DateTime
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    tg_id: Mapped[int] = mapped_column(Integer)

    username: Mapped[str] = mapped_column(String, nullable=True)

    access: Mapped[bool] = mapped_column(Boolean, default=False)

    ads_limit: Mapped[int] = mapped_column(Integer)





