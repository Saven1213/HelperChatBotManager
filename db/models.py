from datetime import datetime
from typing import Optional, Union

from sqlalchemy import String, Integer, Boolean, Float, DateTime, BigInteger
from sqlalchemy.orm import DeclarativeBase,Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    tg_id: Mapped[int] = mapped_column(BigInteger)

    username: Mapped[str] = mapped_column(String, nullable=True)

    ads_limit: Mapped[int] = mapped_column(Integer)

class Group(Base):
    __tablename__ = 'target_groups'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    district: Mapped[str] = mapped_column(String)

    group_id: Mapped[int] = mapped_column(BigInteger)

    name: Mapped[str] = mapped_column(String)

    url: Mapped[str] = mapped_column(String)

class Message(Base):
    __tablename__ = 'messages'


    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    message_id: Mapped[int] = mapped_column(Integer)

    type: Mapped[str] = mapped_column(String)

    chat_id: Mapped[int] = mapped_column(BigInteger)

    time: Mapped[datetime] = mapped_column(DateTime)

    status: Mapped[str] = mapped_column(String)








