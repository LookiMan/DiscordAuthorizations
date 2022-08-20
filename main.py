"""
Завдання: написати пітон скрипт, який автоматично створює discord аккаунт і логіниться в нього отримуючи token авторизації з headers “authorization”
Умови:
- cкрипт повинен приймати емейл та нікнейм у командному рядку
- пароль генерується автоматично
- підтверджувати пошту не треба
Очікується
- повинен створюватися обліковий запис і повертати в командний рядок token після логіну

"""

from art import tprint
from colorama import init, Fore

from robot import init_discord_robot
from utils import (
    Credentials,
    register_user,
    create_password,
    safe_input,
)


init(autoreset=True)


def main():
    tprint("Discord Auth")

    email = safe_input("Insert email")
    username = safe_input("Insert username")

    creds = Credentials(
        email=email,
        username=username,
        password=create_password(),
    )

    token = register_user(creds)

    if not token:
        print(Fore.RED + "[!] Failed to get the user token")
        exit(1)

    print(Fore.GREEN + f"[i] User token: {token}")

    discord_robot = init_discord_robot()

    try:
        discord_robot.login(token)
    except Exception as exc:
        print(Fore.RED + f"[!]: {exc}")
    finally:
        discord_robot.close()


if __name__ == "__main__":
    main()
