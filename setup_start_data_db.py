import asyncio

from sqlalchemy import select

from db.database import async_session
from db.models import Group

groups = {
    -1003738787159: {
        'district': 'Краснодарский край',
        'name': 'Сочи | Доска объявлений | Классифайд ',
        'url': 'https://t.me/Sochi_Lavanda'
    },
    -1003700159735: {
    'district': 'Краснодарский край',
    'name': 'Славянск-на-Кубани | Доска объявлений',
    'url': 'https://t.me/Slavyansk_na_Kubani_Lavanda'
    },
    -1003638151222: {
    'district': 'Краснодарский край',
    'name': 'Приморско-Ахтарск | Доска объявлений',
    'url': 'https://t.me/Primorsko_Akhtarsk_Lavanda'
    },
    -1003587355284: {
    'district': 'Краснодарский край',
    'name': 'Новороссийск | Доска объявлений ',
    'url': 'https://t.me/Novorossiisk_Lavanda'
    },
    -1003516436714: {
    'district': 'Краснодарский край',
    'name': 'Новокубанск | Доска объявлений ',
    'url': 'https://t.me/Novokubansk_Lavanda'
    },
    -1003305231715: {
    'district': 'Краснодарский край',
    'name': 'Лабинск | Доска объявлений | Классифайд ',
    'url': 'https://t.me/Labinsk_Lavanda'
    },
    -1003863854434: {
    'district': 'Краснодарский край',
    'name': 'Курганинск | Доска объявлений | ',
    'url': 'https://t.me/Kurganinsk_Lavanda'
    },
    -1003868329391: {
    'district': 'Краснодарский край',
    'name': 'Ейск | Доска объявлений | Классифайд ',
    'url': 'https://t.me/Eisk_Lavanda'
    },
    -1003889957659: {
    'district': 'Краснодарский край',
    'name': 'Гулькевичи | Доска объявлений ',
    'url': 'https://t.me/Gulkevichi_Lavanda'
    },
    -1003886782445: {
    'district': 'Краснодарский край',
    'name': 'Горячий ключ | Доска объявлений ',
    'url': 'https://t.me/Goryachii_Klyuch_Lavanda'
    },
    -1003838516146: {
    'district': 'Краснодарский край',
    'name': 'Геленджик | Доска объявлений | ',
    'url': 'https://t.me/Gelendzhik_Lavanda'
    },
    -1003837003986: {
    'district': 'Краснодарский край',
    'name': 'Белореченск | Доска объявлений ',
    'url': 'https://t.me/Belorechensk_Lavanda'
    },
    -1003811849643: {
    'district': 'Краснодарский край',
    'name': 'Апшеронск | Доска объявлений | ',
    'url': 'https://t.me/Apsheronsk_Lavanda'
    },
    -1003797404863: {
    'district': 'Краснодарский край',
    'name': 'Анапа | Доска объявлений | Классифайд ',
    'url': 'https://t.me/Anapa_Lavanda'
    }
}


# {
#     'district': '',
#     'name': '',
#     'url': ''
# }

async def add_to_db():
    async with async_session() as session:
        for id_, data in groups.items():
            res = await session.execute(select(Group).where(Group.group_id == id_))
            group_db = res.scalar_one_or_none()
            if group_db:
                print(f'Группа: {group_db.name} уже существует')
            else:
                group = Group(
                    district=data.get('district'),
                    name=data.get('name'),
                    url=data.get('url'),
                    group_id=id_
                )
                print(f'Группа {data.get("name")} успешно добавлена')

                session.add(group)

        await session.commit()

if __name__ == '__main__':
    asyncio.run(add_to_db())