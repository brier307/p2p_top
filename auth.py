from telethon import TelegramClient
from telethon.errors import SessionPasswordNeededError

from config import (
    api_id_check, api_hash_check, phone_number_check,
    api_id_main, api_hash_main, phone_number_main
)


# Функція авторизації для check акаунту
async def auth_check_account():
    client = TelegramClient('session_check', api_id_check, api_hash_check)

    try:
        print("Авторизація check акаунту...")
        await client.connect()

        if not await client.is_user_authorized():
            await client.send_code_request(phone_number_check)
            print("Код авторизації відправлено на номер", phone_number_check)

            while True:
                try:
                    code = input("Введіть код авторизації для check акаунту: ")
                    await client.sign_in(phone_number_check, code)
                    break
                except SessionPasswordNeededError:
                    password = input("Потрібен 2FA пароль для check акаунту: ")
                    await client.sign_in(password=password)
                    break
                except Exception as e:
                    print(f"Помилка при введенні коду: {e}")
                    print("Спробуйте ще раз")

        print("Check акаунт успішно авторизовано!")
        return client

    except Exception as e:
        print(f"Помилка при авторизації check акаунту: {e}")
        return None


# Функція авторизації для main акаунту
async def auth_main_account():
    client = TelegramClient('session_main', api_id_main, api_hash_main)

    try:
        print("Авторизація main акаунту...")
        await client.connect()

        if not await client.is_user_authorized():
            await client.send_code_request(phone_number_main)
            print("Код авторизації відправлено на номер", phone_number_main)

            while True:
                try:
                    code = input("Введіть код авторизації для main акаунту: ")
                    await client.sign_in(phone_number_main, code)
                    break
                except SessionPasswordNeededError:
                    password = input("Потрібен 2FA пароль для main акаунту: ")
                    await client.sign_in(password=password)
                    break
                except Exception as e:
                    print(f"Помилка при введенні коду: {e}")
                    print("Спробуйте ще раз")

        print("Main акаунт успішно авторизовано!")
        return client

    except Exception as e:
        print(f"Помилка при авторизації main акаунту: {e}")
        return None
