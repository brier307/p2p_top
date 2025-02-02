import asyncio
import re

from auth import auth_check_account, auth_main_account
from config import your_nik

top_nick = ''
top_price = None


# Функція для отримання суми для моніторингу від користувача
def get_order_amount():
    while True:
        amount = input("Введіть суму для моніторингу (тільки цифри): ")
        if amount.isdigit():
            return amount
        print("Будь ласка, введіть тільки цифри!")


async def main():
    # Авторизація обох акаунтів
    client_check = await auth_check_account()
    if not client_check:
        print("Помилка авторизації check акаунту")
        return

    client_main = await auth_main_account()
    if not client_main:
        print("Помилка авторизації main акаунту")
        await client_check.disconnect()
        return

    # Отримання суми від користувача
    order_amount = get_order_amount()

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
                        if "Tether" in button.text:  # Перевіряємо, чи є "Tether" у тексті кнопки
                            await button.click()  # Натискаємо кнопку
                            print(f"Натиснуто кнопку: {button.text}")
                            await asyncio.sleep(0.5)
        # Обираємо "Monobank"
        async for message in client_check.iter_messages('CryptoBot', limit=1):
            if message.buttons:
                for row in message.buttons:
                    for button in row:
                        if "Monobank" in button.text:  # Перевіряємо, чи є "Monobank" у тексті кнопки
                            await button.click()  # Натискаємо кнопку
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
                found = False  # Додаємо flag
                for row in message.buttons:
                    if found:  # Перевіряємо flag
                        break
                    for button in row:
                        print(f"{button.text}")
                        if "₴" in button.text:
                            # Використовуємо регулярний вираз для пошуку ціни та ніку
                            match = re.search(r"([A-Za-z0-9_\s]+)\s*·\s*₴([0-9.]+)", button.text)
                            if match:
                                top_nick = match.group(1).strip()  # Нікнейм до "₴"
                                top_price = float(match.group(2))  # Ціна після "₴"
                                print(f"Нікнейм: {top_nick}, Ціна: {top_price}")
                                found = True
                                break  # Виходимо з внутрішнього циклу

        if top_nick != your_nik:

            # Робота з ботом через перший акаунт
            await client_main.send_message('CryptoBot', '/p2p')
            await asyncio.sleep(0.5)

            # Натискаємо "Объявления"
            async for message in client_main.iter_messages('CryptoBot', limit=1):
                if message.buttons:
                    for row in message.buttons:
                        for button in row:
                            if "Объявления" in button.text:  # Перевіряємо, чи є "Объявления" у тексті кнопки
                                await button.click()  # Натискаємо кнопку
                                print(f"Натиснуто кнопку: {button.text}")
                                await asyncio.sleep(0.5)

            # Читання та вибір необхідного оголошення
            async for message in client_main.iter_messages('CryptoBot', limit=1):
                if message.buttons:
                    found = False  # Додаємо прапорець
                    for row in message.buttons:
                        if found:  # Перевіряємо прапорець
                            break
                        for button in row:
                            print(f"{button.text}")
                            if "₴" in button.text:
                                # Використовуємо регулярний вираз для оголшення де є покупка
                                match = re.search(r"Покупка.*₴", button.text)
                                if match:
                                    await button.click()
                                    found = True
                                    print(f"Натиснуто кнопку: {button.text}")
                                    break  # Виходимо з внутрішнього циклу

            # Натискаємо "Цена"
            async for message in client_main.iter_messages('CryptoBot', limit=1):
                if message.buttons:
                    for row in message.buttons:
                        for button in row:
                            if "Цена" in button.text:  # Перевіряємо, чи є "Цена" у тексті кнопки
                                await button.click()  # Натискаємо кнопку
                                print(f"Натиснуто кнопку: {button.text}")
                                await asyncio.sleep(0.5)

            # Відпрака боту ціни

            # Нова ціна
            new_price = top_price + 0.01

            await client_main.send_message('CryptoBot', str(new_price))
            print("Виставлено ціну:", new_price)
            await asyncio.sleep(0.5)

            async for message in client_main.iter_messages('CryptoBot', limit=1):
                if message.buttons:
                    for row in message.buttons:
                        for button in row:
                            if "Сохранить изменения" in button.text:  # Перевіряємо, чи є "Сохранить изменения"
                                await button.click()  # Натискаємо кнопку
                                print(f"Натиснуто кнопку: {button.text}")
                                await asyncio.sleep(0.5)

        else:
            print(your_nik, "на першій позиції")
            pass

    except Exception as e:
        print(f"Помилка під час виконання: {e}")

if __name__ == '__main__':
    asyncio.run(main())