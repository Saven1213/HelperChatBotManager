from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from db.crud.user import get_user, add_user
from handlers.config import tg_id_list

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    tg_id = message.from_user.id

    username = message.from_user.username

    user = await get_user(tg_id)

    if not user:
        await add_user(tg_id, username)

    if tg_id in tg_id_list:

        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Посмотреть список всех групп')
                ]
            ]
        )

        await message.answer('Добро пожаловать в админ панель хелпера!', reply_markup=)
        return

    text = ('👋 <b>Добро пожаловать в бот-доступа чатов Москвы и Подмосковья</b>\n\n'
            'В наших чатах Вы можете опубликовать своё объявление и найти покупателей на ваши товары или услуги.\n\n'
            'Размещая у нас объявление, Вы автоматически соглашаетесь с <a href="https://telegra.ph/Polzovatelskoe-soglashenie-ob-usloviyah-ispolzovaniya-Klassifajd-chatov-05-20">Договором-офертой</a>. '
            'Если Вы не согласны с офертой, то пожалуйста покиньте чат.\n\n'
            'Наши чаты работают по принципу площадок Классифайд - досок объявлений, как Avito, Cian и т.д. '
            'Для обычных объявлений маркировка не требуется (разъяснение ФАС №АК-83509-19 от 25.09.2019, п.2.2.). '
            'В чате все объявления размещаются в обычном едином стиле, без внешних ссылок. '
            'Допустимое кол-во символов не более 1000.\n\n'
            '❗️<b>Вы можете размещать объявления в любых чатах нашей сети!</b>\n'
            'Добавьте папку с чатами и публикуйте объявления во всех чатах по единому тарифу '
            '<a href="https://t.me/addlist/UHtNsWRvduxhNjNi">https://t.me/addlist/UHtNsWRvduxhNjNi</a>')

    await message.answer(text=text)

    keyboard = InlineKeyboardMarkup(inline_keyboard=[

        [
            InlineKeyboardButton(text="10 объявлений за 200р.", callback_data="price-200")
        ],
        [
            InlineKeyboardButton(text="100 объявлений за 1'000р.", callback_data="price-1000")
        ],
        [
            InlineKeyboardButton(text="999 объявлений за 5'000р.", callback_data="price-5000")
        ]
    ])


    text2 = ('⬇️ <b>Выберите тариф:</b>\n\n'
            '<b>Тариф «Стартовый»</b> ⤵️\n'
            '10 объявлений за 200р.\n\n'
            '<b>Тариф «Оптимальный»</b> ⤵️\n'
            '100 объявлений за 1\'000р.\n\n'
            '<b>Тариф «Максимальный»</b> ⤵️\n'
            '999 объявлений за 5\'000р.\n\n'
            '⚠️ Тарифы действуют на всю сеть чатов, то есть, купив тариф, вы сможете размещать объявления в любом из 54 чатов сети 👉 '
            '<a href="https://t.me/addlist/UHtNsWRvduxhNjNi">https://t.me/addlist/UHtNsWRvduxhNjNi</a>\n\n'
            '🔥 Реклама с закрепом ➡️ @ads_moscow_bot')



    await message.answer(text2, reply_markup=keyboard)
