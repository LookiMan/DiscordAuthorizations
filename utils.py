from random import choices
from string import printable
from dataclasses import dataclass


from colorama import Fore


@dataclass
class Credentials:
    email: str
    username: str
    password: str


def safe_input(caption: str):
    while True:
        print(Fore.GREEN + f"[i] {caption}")

        try:
            result = input("[<] ").strip()
        except KeyboardInterrupt:
            exit(Fore.YELLOW + "[i] Closing script...")
        else:
            if result:
                return result


def create_password(length: int = 8):
    return "".join(choices(list(printable), k=length))
