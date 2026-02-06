from db.database import async_session
from db.models import Payment


async def add_payment(
        tg_id: int,
        payment_id: str,
        payload: str,
        currency: str,
        amount: int
):
    async with async_session() as session:
        payment = Payment(
            tg_id=tg_id,
            payment_id=payment_id,
            payload=payload,
            currency=currency,
            amount=amount
        )

        session.add(payment)

        await session.commit()