import stripe
from forex_python.converter import CurrencyRates

from config import settings

stripe.api_key = settings.API_KEY


def convert_rub_to_usd(amount):
    """ Конвертирует доллары в рубли. """

    try:
        # c = CurrencyRates()
        # rate = c.get_rate('RUB', 'USD')
        return int(amount * 100)
    except Exception as e:
        print(f'Ошибка при конвертации валюты: {e}')
        return 0


def create_stripe_price(amount):
    """ Создает сумму платежа в Stripe. """

    try:
        return stripe.Price.create(
                  currency="usd",
                  unit_amount=amount,
                  product_data={"name": "Payment"},
                )
    except Exception as e:
        print(f'Ошибка при создании цены в Stripe: {e}')
        return None


def create_stripe_session(price):
    """ Создает сессию на оплату в Stripe. """

    try:
        session = stripe.checkout.Session.create(
            success_url="http://127.0.0.1:8000/",
            line_items=[{"price": price.get('id'), "quantity": 1}],
            mode="payment",
        )

        return session.get('id'), session.get('url')
    except Exception as e:
        print(f'Ошибка при создании сессии на оплату в Stripe: {e}')
        return None, None
