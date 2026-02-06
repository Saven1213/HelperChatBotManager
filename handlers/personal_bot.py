import os
from cProfile import label

from aiogram import F, Router, Bot
from aiogram.enums import ContentType
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton, LabeledPrice, \
    PreCheckoutQuery
from dotenv import load_dotenv
from sqlalchemy import select
from aiogram.fsm.state import State, StatesGroup

from db.crud.groups import get_groups, add_group, get_group_by_id, delete_group
from db.crud.payment import add_payment
from db.crud.user import get_user, add_user, add_ad
from db.database import async_session
from db.models import Group
from handlers.config import tg_id_list

router = Router()

load_dotenv()

YOOTOKEN = os.getenv("YOOTOKEN")



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
                    InlineKeyboardButton(text='Посмотреть список всех групп', callback_data='groups_list')
                ]
            ]
        )

        await message.answer('Добро пожаловать в админ панель хелпера!', reply_markup=keyboard)
        return

    text = ('👋 <b>Добро пожаловать в бот-доступа чатов Москвы и Подмосковья</b>\n\n'
            'В наших чатах Вы можете опубликовать своё объявление и найти покупателей на ваши товары или услуги.\n\n'
            'Размещая у нас объявление, Вы автоматически соглашаетесь с <a href="https://telegra.ph/Oferta-na-okazanie-uslug-po-razmeshcheniyu-reklamy-v-Klassifajd-chatah-02-03">Договором-офертой</a>. '
            'Если Вы не согласны с офертой, то пожалуйста покиньте чат.\n\n'
            'Наши чаты работают по принципу площадок Классифайд - досок объявлений, как Avito, Cian и т.д. '
            'Для обычных объявлений маркировка не требуется (разъяснение ФАС №АК-83509-19 от 25.09.2019, п.2.2.). '
            'В чате все объявления размещаются в обычном едином стиле, без внешних ссылок. '
            'Допустимое кол-во символов не более 1000.\n\n'
            '❗️<b>Вы можете размещать объявления в любых чатах нашей сети!</b>\n'
            'Добавьте папку с чатами и публикуйте объявления во всех чатах по единому тарифу '
            '<a href="https://t.me/addlist/8fGeGpWoxMVkNWIy">https://t.me/addlist/8fGeGpWoxMVkNWIy</a>')

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
            'https://t.me/addlist/8fGeGpWoxMVkNWIy\n\n'
            '🔥 Реклама с закрепом ➡️ @Lavanda_ads_bot')



    await message.answer(text2, reply_markup=keyboard)


@router.callback_query(F.data == 'main')
async def main(callback: CallbackQuery, state: FSMContext):
    await state.clear()

    tg_id = callback.from_user.id

    username = callback.from_user.username

    user = await get_user(tg_id)

    if not user:
        await add_user(tg_id, username)

    if tg_id in tg_id_list:
        keyboard = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(text='Посмотреть список всех групп', callback_data='groups_list')
                ]
            ]
        )

        await callback.message.answer('Добро пожаловать в админ панель хелпера!', reply_markup=keyboard)
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
            'https://t.me/addlist/8fGeGpWoxMVkNWIy')

    await callback.message.answer(text=text)

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
             'https://t.me/addlist/8fGeGpWoxMVkNWIy\n\n'
             '🔥 Реклама с закрепом ➡️ @Lavanda_ads_bot')

    await callback.message.answer(text2, reply_markup=keyboard)


@router.callback_query(F.data.startswith('groups_list'))
async def groups_list_simple(callback: CallbackQuery):
    """Упрощенный вариант с пагинацией"""
    page = 1

    if '_' in callback.data:
        try:
            page = int(callback.data.split('_')[2])
        except:
            pass

    items_per_page = 6
    offset = (page - 1) * items_per_page

    async with async_session() as session:

        result = await session.execute(
            select(Group)
            .order_by(Group.id)
            .limit(items_per_page + 1)
            .offset(offset)
        )
        groups = result.scalars().all()

    keyboard = InlineKeyboardMarkup(inline_keyboard=[])


    groups_to_show = groups[:items_per_page]

    if groups_to_show:
        for group in groups_to_show:
            keyboard.inline_keyboard.append([
                InlineKeyboardButton(
                    text=f"📁 {group.name}",
                    callback_data=f"group-{group.id}"
                )
            ])

    # Добавляем пагинацию
    pagination_row = []

    # Есть ли предыдущая страница?
    if page > 1:
        pagination_row.append(
            InlineKeyboardButton(
                text="◀️",
                callback_data=f"groups_list_{page - 1}"
            )
        )

    # Есть ли следующая страница? (проверяем по 7-й группе)
    has_next_page = len(groups) > items_per_page
    if has_next_page:
        pagination_row.append(
            InlineKeyboardButton(
                text="▶️",
                callback_data=f"groups_list_{page + 1}"
            )
        )

    if pagination_row:
        keyboard.inline_keyboard.append(pagination_row)


    keyboard.inline_keyboard.append([
        InlineKeyboardButton(
            text="➕ Создать группу",
            callback_data="add_new_group"
        )
    ])


    if groups_to_show:
        text = f"📋 Группы (стр. {page})"
    else:
        text = "📭 Нет групп. Создайте первую!"

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )
    await callback.answer()


class NewGroup(StatesGroup):
    id_ = State()
    name = State()
    url = State()
    district = State()


@router.callback_query(F.data == 'add_new_group')
async def add_new_group(callback: CallbackQuery, state: FSMContext):
    await state.set_state(NewGroup.id_)
    await callback.message.edit_text(
        "🔢 Введите ID группы (число):",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="main")]
        ])
    )
    await callback.answer()


@router.message(NewGroup.id_)
async def process_group_id(message: Message, state: FSMContext):
    await state.update_data(id_=message.text)
    await state.set_state(NewGroup.name)
    await message.answer("📝 Введите название группы:")


@router.message(NewGroup.name)
async def process_group_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(NewGroup.url)
    await message.answer("🔗 Введите URL группы:")


@router.message(NewGroup.url)
async def process_group_url(message: Message, state: FSMContext):
    await state.update_data(url=message.text)
    await state.set_state(NewGroup.district)
    await message.answer("📍 Введите район (округ):")


@router.message(NewGroup.district)
async def process_group_district(message: Message, state: FSMContext):
    data = await state.get_data()

    name = data.get('name')
    url = data.get('url')
    id_ = int(data.get('id_'))
    district = message.text

    await add_group(id_, name, url, district)


    await message.answer(
        f"✅ Данные группы собраны:\n\n"
        f"<b>ID:</b> {id_}\n"
        f"<b>Название:</b> {name}\n"
        f"<b>URL:</b> {url}\n"
        f"<b>Район:</b> {district}"
    )

    await state.clear()


@router.callback_query(F.data.split('-')[0] == 'group')
async def group_info(callback: CallbackQuery):
    """Информация о конкретной группе"""

    parts = callback.data.split('-')


    try:
        group_id = int(parts[1])
    except ValueError:
        await callback.answer("❌ Неверный ID группы")
        return

    # Получаем группу из БД
    group = await get_group_by_id(group_id)

    if not group:
        await callback.message.edit_text(
            "❌ Группа не найдена",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ Назад", callback_data="groups_list")]
            ])
        )
        await callback.answer()
        return

    # Формируем информацию о группе
    info_text = (
        f"📋 <b>Информация о группе</b>\n\n"
        f"🆔 ID в БД: <code>{group.id}</code>\n"
        f"📎 ID группы: <code>{group.group_id}</code>\n"
        f"📝 Название: {group.name}\n"
        f"📍 Район: {group.district or 'Не указан'}\n"
        f"🔗 URL: {group.url or 'Не указан'}\n"
    )

    # Добавляем статистику если есть поля
    if hasattr(group, 'member_count'):
        info_text += f"👥 Участников: {group.member_count or 'Неизвестно'}\n"

    if hasattr(group, 'created_at'):
        info_text += f"📅 Создана: {group.created_at.strftime('%d.%m.%Y')}\n"


    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🗑️ Удалить", callback_data=f"delete_confirm-{group.id}")
        ],
        [
            InlineKeyboardButton(text="⬅️ К списку групп", callback_data="groups_list"),
            InlineKeyboardButton(text="🏠 Главное меню", callback_data="main")
        ]
    ])

    await callback.message.edit_text(
        text=info_text,
        reply_markup=keyboard
    )
    await callback.answer()


@router.callback_query(F.data.split('-')[0] == 'delete_confirm')
async def delete_group_confirm(callback: CallbackQuery):

    parts = callback.data.split('-')


    try:
        group_id = int(parts[1])
    except ValueError:
        await callback.answer("❌ Неверный ID группы")
        return

    group = await get_group_by_id(group_id)

    if not group:
        await callback.answer("❌ Группа не найдена")
        return

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Да, удалить", callback_data=f"delete_group-{group_id}"),
            InlineKeyboardButton(text="❌ Нет, отмена", callback_data=f"group-{group_id}")
        ]
    ])

    await callback.message.edit_text(
        text=f"⚠️ <b>Вы уверены что хотите удалить группу?</b>\n\n"
             f"<code>{group.name}</code>\n\n"
             f"Это действие нельзя отменить!",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()


@router.callback_query(F.data.split('-')[0] == 'delete_group')
async def delete_group_handler(callback: CallbackQuery):
    """Удаление группы"""
    parts = callback.data.split('-')


    try:
        group_id = int(parts[1])
    except ValueError:
        await callback.answer("❌ Неверный ID группы")
        return


    group = await delete_group(group_id)

    if group:
        await callback.message.edit_text(
            text=f"✅ Группа <code>{group.name}</code> удалена",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ К списку групп", callback_data="groups_list")]
            ])
    )
    else:
        await callback.message.edit_text(
            text="❌ Группа не найдена",
            reply_markup=InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text="⬅️ К списку групп", callback_data="groups_list")]
            ])
        )

    await callback.answer()

@router.callback_query(F.data.split('-')[0] == 'price')
async def price_handle(callback: CallbackQuery):
    price = int(callback.data.split('-')[1])

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=f'💳 Оплатить {price} Р', callback_data=f'process_payment-{price}')
            ],
            [
                InlineKeyboardButton(text='🏠 Главное меню', callback_data='main')
            ]
        ]
    )

    text = (
        '10 объявлений за 200р.\n'
        'Цена: 200 руб\n'
        'Кол-во доступных сообщений: 10\n\n'

        '✅ '
        'Опубликуйте 10 объявлений в <a href="https://t.me/addlist/8fGeGpWoxMVkNWIy">26-ти чатах нашей сети</a>\n\n'

        '📝 Требования к сообщениям в чатах:\n'
        '✓ Количество символов до 1000\n'
        '✓ Без указания внешних ссылок\n'
        '✓ Запрещены репосты и кнопки\n\n'
        '💬 Остались вопросы? Пишите\n'
        '👉 @maks_manshilin\n\n'

        '🔥 Вы можете размешать объявления во всех <a href="https://t.me/addlist/8fGeGpWoxMVkNWIy">26-ти чатах нашей сети</a>\n\n'
        

        '⬇️ Для оплаты тарифа нажмите кнопку ниже'
    )

    await callback.message.edit_text(text=text, reply_markup=keyboard)
@router.callback_query(F.data.split("-")[0] == 'process_payment')
async def process_payment(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()

    price = callback.data.split('-')[1]

    tg_id = callback.from_user.id
    await bot.send_invoice(
        chat_id=tg_id,
        title='Оплата доступа',
        description='Оплата за доступ к размещению объявлений',
        payload='pay_ads',
        provider_token=str(YOOTOKEN),
        currency="RUB",
        start_parameter='pay_ads',
        prices=[
            LabeledPrice(label='К оплате', amount=int(price) * 100)
        ]
    )

@router.pre_checkout_query()
async def process_the_checkout_query(checkout: PreCheckoutQuery, bot: Bot):
    await bot.answer_pre_checkout_query(checkout.id, ok=True)

@router.message(F.successful_payment)
async def if_success(message: Message):
    payment = message.successful_payment
    tg_id = message.from_user.id
    if payment.invoice_payload == "pay_ads":


        amount = payment.total_amount // 100
        ads = 0

        if amount == 200:
            ads += 10
        elif amount == 1000:
            ads += 100
        elif amount == 5000:
            ads += 999


        await add_ad(tg_id, ads)

        payment_id = payment.provider_payment_charge_id
        payment_currency = payment.currency
        payment_payload = payment.invoice_payload

        await add_payment(tg_id, payment_id, payment_payload, payment_currency, amount)


        await message.answer(
            f"✅ Оплата прошла успешно\n"
            f"📦 Начислено объявлений: {ads}"
        )




