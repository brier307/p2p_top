import asyncio
import re
import time

from auth import auth_check_account, auth_main_account
from config import your_nik

top_nick = ''
top_price = None


def get_order_amount():
    while True:
        amount = input("Введіть суму для моніторингу (тільки цифри): ")
        if amount.isdigit():
            return amount
        print("Будь ласка, введіть тільки цифри!")


async def main_loop():
    # Отримання суми від користувача (тільки один раз перед циклом)
    order_amount = get_order_amount()

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

                # Відправка суми
                await client_check.send_message('CryptoBot', order_amount)
                await asyncio.sleep(0.5)

                # Читання та виведення тексту кнопок з цінами
                async for message in client_check.iter_messages('CryptoBot', limit=1):
                    if message.buttons:
                        found = False
                        for row in message.buttons:
                            if found:
                                break
                            for button in row:
                                print(f"{button.text}")
                                if "₴" in button.text:
                                    match = re.search(r"([A-Za-z0-9_\s]+)\s*·\s*₴([0-9.]+)", button.text)
                                    if match:
                                        top_nick = match.group(1).strip()
                                        top_price = float(match.group(2))
                                        print(f"Нікнейм: {top_nick}, Ціна: {top_price}")
                                        found = True
                                        break

                if top_nick != your_nik:
                    # Робота з ботом через перший акаунт
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
                                        match = re.search(r"Продажа.*₴", button.text)
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

                    # Нова ціна
                    new_price = top_price + 0.01

                    await client_main.send_message('CryptoBot', str(new_price))
                    print("Виставлено ціну:", new_price)
                    await asyncio.sleep(0.5)

                    async for message in client_main.iter_messages('CryptoBot', limit=1):
                        if message.buttons:
                            for row in message.buttons:
                                for button in row:
                                    if "Сохранить изменения" in button.text:
                                        await button.click()
                                        print(f"Натиснуто кнопку: {button.text}")
                                        await asyncio.sleep(0.5)

                else:
                    print(your_nik, "на першій позиції")

                # Чекаємо 3 хвилини перед наступною ітерацією
                print("Очікування 3 хвилини перед наступною перевіркою...")
                await asyncio.sleep(180)  # 3 хвилини = 180 секунд

            except Exception as e:
                print(f"Помилка під час виконання: {e}")
                print("Очікування 20 секунд перед повторною спробою...")
                await asyncio.sleep(20)

    finally:
        # Відключаємо клієнти тільки при повному завершенні програми
        await client_check.disconnect()
        await client_main.disconnect()


if __name__ == '__main__':
    asyncio.run(main_loop())