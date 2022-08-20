from random import choices
from string import printable
from dataclasses import dataclass
from typing import Optional

from requests import post
from colorama import Fore
from twocaptcha import TwoCaptcha

from config import CAPTCHA_API_TOKEN


solver = TwoCaptcha(CAPTCHA_API_TOKEN)

@dataclass
class Credentials:
    email: str
    username: str
    password: str


def safe_input(caption: str) -> str:
    while True:
        print(Fore.GREEN + f"[i] {caption}")

        try:
            result = input("[<] ").strip()
        except KeyboardInterrupt:
            exit(Fore.YELLOW + "[i] Closing script...")
        else:
            if result:
                return result


def create_password(length: int = 10) -> str:
    return "".join(choices(list(printable), k=length))


def register_user(credentials: Credentials) -> Optional[str]:
    result = solver.hcaptcha(
        sitekey="4c672d35-0701-42b2-88c3-78380b0db560",
        url="https://discord.com/register",
    )

    response = post("https://discord.com/api/v9/auth/register", json={
        "captcha_key": result.get("code"),
        "consent": True,
        "date_of_birth": "1988-04-05",
        "email": credentials.email,
        "gift_code_sku_id": None,
        "invite": None,
        "password":  credentials.password,
        "promotional_email_opt_in": False,
        "username": credentials.username
    })

    return response.json().get("token")


