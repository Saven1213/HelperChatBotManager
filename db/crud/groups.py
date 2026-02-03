from dataclasses import asdict


from sqlalchemy import select

from db.database import async_session
from db.models import Group


async def get_groups():
    async with async_session() as session:
        res = await session.execute(select(Group))

        groups = res.scalars().all()

        return groups

async def add_group(id_: int, name: str, url: str, district: str):
    async with async_session() as session:
        group = Group(
            group_id=id_,
            name=name,
            district=district,
            url=url
        )

        session.add(group)

        await session.commit()

async def get_group_by_id(id_: int):
    async with async_session() as session:
        res = await session.execute(select(Group).where(Group.id == id_))

        group = res.scalar_one_or_none()

        return group


async def delete_group(group_id):
    async with async_session() as session:
        result = await session.execute(
            select(Group).where(Group.id == group_id)
        )
        group = result.scalar_one_or_none()

        if group:
            await session.delete(group)
            await session.commit()
            return group