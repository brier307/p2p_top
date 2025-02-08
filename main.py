import asyncio
import re
import random

from auth import auth_check_account, auth_main_account
from config import your_nick

top_nick_uah = ''
top_price_uah = None
second_nick_uah = ''
second_price_uah = None

top_nick_kzt = ''
top_price_kzt = None
second_nick_kzt = ''
second_price_kzt = None


def random_time_circle():
    return random.randint(90, 1200)


def get_order_amount_uah():
    while True:
        amount_uah = input("Введіть суму для моніторингу UAH(тільки цифри): ")
        if amount_uah.isdigit():
            return amount_uah
        print("Будь ласка, введіть тільки цифри!")


def get_order_amount_kzt():
    while True:
        amount_kzt = input("Введіть суму для моніторингу KZT(тільки цифри): ")
        if amount_kzt.isdigit():
            return amount_kzt
        print("Будь ласка, введіть тільки цифри!")


async def update_price_uah(client_main, new_price_uah):
    """Вспомогательная функция для обновления цены"""
    await client_main.send_message('CryptoBot', '/p2p')
    await asyncio.sleep(0.5)

    # Натискаємо "Объявления"
    async for message in client_main.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "Объявления" in button.text:
                        await button.click()
                        print(f"Натиснуто кнопку: {button.text}")
                        await asyncio.sleep(0.5)

    # Читання та вибір необхідного оголошення
    async for message in client_main.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            found = False
            for row in message.buttons:
                if found:
                    break
                for button in row:
                    print(f"{button.text}")
                    if "₴" in button.text:
                        match = re.search(r"Покупка.*USDT.*₴", button.text)
                        if match:
                            await button.click()
                            found = True
                            print(f"Натиснуто кнопку: {button.text}")
                            break

    # Натискаємо "Цена"
    async for message in client_main.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "Цена" in button.text:
                        await button.click()
                        print(f"Натиснуто кнопку: {button.text}")
                        await asyncio.sleep(0.5)

    new_price_uah = round(new_price_uah, 2)
    await client_main.send_message('CryptoBot', str(new_price_uah))
    print("Виставлено ціну:", new_price_uah)
    await asyncio.sleep(0.5)

    async for message in client_main.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "Сохранить изменения" in button.text:
                        await button.click()
                        print(f"Натиснуто кнопку: {button.text}")
                        await asyncio.sleep(0.5)


async def update_price_kzt(client_main, new_price_kzt):
    """Вспомогательная функция для обновления цены"""
    await client_main.send_message('CryptoBot', '/p2p')
    await asyncio.sleep(0.5)

    # Натискаємо "Объявления"
    async for message in client_main.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "Объявления" in button.text:
                        await button.click()
                        print(f"Натиснуто кнопку: {button.text}")
                        await asyncio.sleep(0.5)

    # Читання та вибір необхідного оголошення
    async for message in client_main.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            found = False
            for row in message.buttons:
                if found:
                    break
                for button in row:
                    print(f"{button.text}")
                    if "₸" in button.text:
                        match = re.search(r"Покупка.*USDT.*₸", button.text)
                        if match:
                            await button.click()
                            found = True
                            print(f"Натиснуто кнопку: {button.text}")
                            break

    # Натискаємо "Цена"
    async for message in client_main.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "Цена" in button.text:
                        await button.click()
                        print(f"Натиснуто кнопку: {button.text}")
                        await asyncio.sleep(0.5)

    new_price_kzt = round(new_price_kzt, 2)
    await client_main.send_message('CryptoBot', str(new_price_kzt))
    print("Виставлено ціну:", new_price_kzt)
    await asyncio.sleep(0.5)

    async for message in client_main.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "Сохранить изменения" in button.text:
                        await button.click()
                        print(f"Натиснуто кнопку: {button.text}")
                        await asyncio.sleep(0.5)


async def main_loop():
    # Отримання суми від користувача (тільки один раз перед циклом)
    order_amount_uah = get_order_amount_uah()

    order_amount_kzt = get_order_amount_kzt()

    # Авторизація обох акаунтів один раз перед циклом
    client_check = await auth_check_account()
    if not client_check:
        print("Помилка авторизації check акаунту")
        return

    client_main = await auth_main_account()
    if not client_main:
        print("Помилка авторизації main акаунту")
        await client_check.disconnect()
        return

    try:
        while True:
            try:
                # Робота з ботом через перший акаунт
                # Перевірка валюти обраної маркету

                await client_check.send_message('CryptoBot', '/p2p')
                await asyncio.sleep(0.5)

                await check_if_uah(client_check)  # Проверка/переключение валюты на UAH

                await client_check.send_message('CryptoBot', '/p2p')
                await asyncio.sleep(0.5)

                # Очікування відповіді від бота та натискання кнопки "Продать"
                async for message in client_check.iter_messages('CryptoBot', limit=1):
                    if message.buttons:
                        for row in message.buttons:
                            for button in row:
                                if button.text == "📉 Продать":
                                    await button.click()
                                    print(f"Натиснуто кнопку: {button.text}")
                                    await asyncio.sleep(0.5)
                # Обираємо "Tether"
                async for message in client_check.iter_messages('CryptoBot', limit=1):
                    if message.buttons:
                        for row in message.buttons:
                            for button in row:
                                if "Tether" in button.text:
                                    await button.click()
                                    print(f"Натиснуто кнопку: {button.text}")
                                    await asyncio.sleep(0.5)
                # Обираємо "Monobank"
                async for message in client_check.iter_messages('CryptoBot', limit=1):
                    if message.buttons:
                        for row in message.buttons:
                            for button in row:
                                if "Monobank" in button.text:
                                    await button.click()
                                    print(f"Натиснуто кнопку: {button.text}")
                                    await asyncio.sleep(0.5)
                # Вказання суми
                async for message in client_check.iter_messages('CryptoBot', limit=1):
                    if message.buttons:
                        for row in message.buttons:
                            for button in row:
                                if "Указать сумму" in button.text:
                                    await button.click()
                                    print(f"Натиснуто кнопку: {button.text}")
                                    await asyncio.sleep(0.5)

                # Відправка суми в UAH
                await client_check.send_message('CryptoBot', order_amount_uah)
                await asyncio.sleep(0.5)

                # Читання та виведення тексту кнопок з цінами
                async for message in client_check.iter_messages('CryptoBot', limit=1):
                    if message.buttons:
                        sellers_found = 0
                        for row in message.buttons:
                            if sellers_found >= 2:
                                break
                            for button in row:
                                print(f"{button.text}")
                                if "₴" in button.text:
                                    match = re.search(r"([A-Za-z0-9_\s]+)\s*·\s*₴([0-9.]+)", button.text)
                                    if match:
                                        if sellers_found == 0:
                                            global top_nick_uah, top_price_uah
                                            top_nick_uah = match.group(1).strip()
                                            top_price_uah = float(match.group(2))
                                            print(f"Перший продавець - Нікнейм: {top_nick_uah}, Ціна: {top_price_uah}")
                                        elif sellers_found == 1:
                                            global second_nick_uah, second_price_uah
                                            second_nick_uah = match.group(1).strip()
                                            second_price_uah = float(match.group(2))
                                            print(f"Другий продавець - Нікнейм: {second_nick_uah}, Ціна: {second_price_uah}")
                                        sellers_found += 1
                                        if sellers_found >= 2:
                                            break

                await check_if_kzt(client_check)  # Проверка/переключение валюты на KZT

                await client_check.send_message('CryptoBot', '/p2p')
                await asyncio.sleep(0.5)

                # Очікування відповіді від бота та натискання кнопки "Продать"
                async for message in client_check.iter_messages('CryptoBot', limit=1):
                    if message.buttons:
                        for row in message.buttons:
                            for button in row:
                                if button.text == "📉 Продать":
                                    await button.click()
                                    print(f"Натиснуто кнопку: {button.text}")
                                    await asyncio.sleep(0.5)
                # Обираємо "Tether"
                async for message in client_check.iter_messages('CryptoBot', limit=1):
                    if message.buttons:
                        for row in message.buttons:
                            for button in row:
                                if "Tether" in button.text:
                                    await button.click()
                                    print(f"Натиснуто кнопку: {button.text}")
                                    await asyncio.sleep(0.5)
                # Обираємо "Kaspi Bank"
                async for message in client_check.iter_messages('CryptoBot', limit=1):
                    if message.buttons:
                        for row in message.buttons:
                            for button in row:
                                if "Kaspi Bank" in button.text:
                                    await button.click()
                                    print(f"Натиснуто кнопку: {button.text}")
                                    await asyncio.sleep(0.5)
                # Вказання суми
                async for message in client_check.iter_messages('CryptoBot', limit=1):
                    if message.buttons:
                        for row in message.buttons:
                            for button in row:
                                if "Указать сумму" in button.text:
                                    await button.click()
                                    print(f"Натиснуто кнопку: {button.text}")
                                    await asyncio.sleep(0.5)

                # Відправка суми в KZT
                await client_check.send_message('CryptoBot', order_amount_kzt)
                await asyncio.sleep(0.5)

                # Читання та виведення тексту кнопок з цінами
                async for message in client_check.iter_messages('CryptoBot', limit=1):
                    if message.buttons:
                        sellers_found = 0
                        for row in message.buttons:
                            if sellers_found >= 2:
                                break
                            for button in row:
                                print(f"{button.text}")
                                if "₸" in button.text:
                                    match = re.search(r"([A-Za-z0-9_\s]+)\s*·\s*₸([0-9.]+)", button.text)
                                    if match:
                                        if sellers_found == 0:
                                            global top_nick_kzt, top_price_kzt
                                            top_nick_kzt = match.group(1).strip()
                                            top_price_kzt = float(match.group(2))
                                            print(f"Перший продавець - Нікнейм: {top_nick_kzt}, Ціна: {top_price_kzt}")
                                        elif sellers_found == 1:
                                            global second_nick_kzt, second_price_kzt
                                            second_nick_uah = match.group(1).strip()
                                            second_price_kzt = float(match.group(2))
                                            print(f"Другий продавець - Нікнейм: {second_nick_kzt}, Ціна: {second_price_kzt}")
                                        sellers_found += 1
                                        if sellers_found >= 2:
                                            break

                # Проверка условий для изменения цены для UAH
                if top_nick_uah == your_nick:
                    print(f"Ви на першій позиції по UAH")
                    # Проверяем, не слишком ли большая разница с вторым местом
                    if second_price_uah and (top_price_uah - second_price_uah) > 0.05:
                        print(f"Різниця з другим місцем по UAH завелика ({top_price_uah - second_price_uah}), змінюємо ціну")
                        new_price_uah = second_price_uah + 0.01
                        await update_price_uah(client_main, new_price_uah)
                    else:
                        print("Різниця з другим місцем по UAH в нормі")
                else:
                    print(f"Ви не на першій позиції по UAH, змінюємо ціну")
                    new_price_uah = top_price_uah + 0.01
                    await update_price_uah(client_main, new_price_uah)

                # Проверка условий для изменения цены для KZT
                if top_nick_kzt == your_nick:
                    print(f"Ви на першій позиції по KZT")
                    # Проверяем, не слишком ли большая разница с вторым местом
                    if second_price_kzt and (top_price_kzt - second_price_kzt) > 0.05:
                        print(f"Різниця з другим місцем по KZT завелика ({top_price_kzt - second_price_kzt}), змінюємо ціну")
                        new_price_kzt = second_price_kzt + 0.01
                        await update_price_kzt(client_main, new_price_kzt)
                    else:
                        print("Різниця з другим місцем по KZT в нормі")
                else:
                    print(f"Ви не на першій позиції по KZT, змінюємо ціну")
                    new_price_kzt = top_price_kzt + 0.01
                    await update_price_kzt(client_main, new_price_kzt)

                # Чекаємо 3 хвилини перед наступною ітерацією
                next_circle = random_time_circle()
                print(f"Очікування {next_circle} секунд перед наступною перевіркою...")
                await asyncio.sleep(next_circle)

            except Exception as e:
                print(f"Помилка під час виконання: {e}")
                print("Очікування 20 секунд перед повторною спробою...")
                await asyncio.sleep(20)

    finally:
        # Відключаємо клієнти тільки при повному завершенні програми
        await client_check.disconnect()
        await client_main.disconnect()


async def check_if_uah(client_check):  # Проверяет валюту на UAH

    await client_check.send_message('CryptoBot', '/p2p')
    await asyncio.sleep(0.5)

    async for message in client_check.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "Оплата и валюта" in button.text:
                        await button.click()
                        print(f"Натиснуто кнопку: {button.text}")
                        await asyncio.sleep(0.5)

    async for message in client_check.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "Валюта P2P Маркета:" in button.text:
                        currency = button.text.split(":")[-1].strip()  # Извлекаем валюту
                        if currency == "UAH":
                            return

    async for message in client_check.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "Валюта P2P Маркета" in button.text:
                        await button.click()
                        print(f"Натиснуто кнопку: {button.text}")
                        await asyncio.sleep(0.5)

    async for message in client_check.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "UAH" in button.text:
                        await button.click()
                        print(f"Натиснуто кнопку: {button.text}")
                        await asyncio.sleep(0.5)


async def check_if_kzt(client_check):  # Проверяет валюту на KZT

    await client_check.send_message('CryptoBot', '/p2p')
    await asyncio.sleep(0.5)

    async for message in client_check.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "Оплата и валюта" in button.text:
                        await button.click()
                        print(f"Натиснуто кнопку: {button.text}")
                        await asyncio.sleep(0.5)

    async for message in client_check.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "Валюта P2P Маркета:" in button.text:
                        currency = button.text.split(":")[-1].strip()  # Извлекаем валюту
                        if currency == "KZT":
                            return

    async for message in client_check.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "Валюта P2P Маркета" in button.text:
                        await button.click()
                        print(f"Натиснуто кнопку: {button.text}")
                        await asyncio.sleep(0.5)

    async for message in client_check.iter_messages('CryptoBot', limit=1):
        if message.buttons:
            for row in message.buttons:
                for button in row:
                    if "KZT" in button.text:
                        await button.click()
                        print(f"Натиснуто кнопку: {button.text}")
                        await asyncio.sleep(0.5)

if __name__ == '__main__':
    asyncio.run(main_loop())
