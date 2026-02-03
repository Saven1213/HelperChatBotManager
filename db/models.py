from typing import Optional, Union

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

class Group(Base):
    __tablename__ = 'target_groups'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    district: Mapped[str] = mapped_column(String)

    group_id: Mapped[int] = mapped_column(Integer)

    name: Mapped[str] = mapped_column(String)

    url: Mapped[str] = mapped_column(String)








