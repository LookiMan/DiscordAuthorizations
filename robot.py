from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By


CHROMEDRIVER_PATH = "./src/chromedriver.exe"


class DiscordRobot(object):
    def __init__(self, wd) -> None:
        self.wd = wd

    def close(self) -> None:
        self.wd.quit()

    def await_element_to_be_clickable(self, css_selector: str, timeout: int=10) -> None:
        wait = WebDriverWait(self.wd, timeout)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))

    def open_tab(self, url: str) -> None:
        self.wd.get(url)

    def close_tab(self) -> None:
        self.wd.close()

    def login(self, token: str) -> None:
        self.open_tab("https://discord.com/login")
        self.await_element_to_be_clickable('form button[type="submit"]')

        self.wd.execute_script(
            f"""
            function login(token) {{
                setInterval(() => {{document.body.appendChild(document.createElement `iframe`).contentWindow.localStorage.token = `"${{token}}"`}}, 50);
                setTimeout(() => {{location.reload();}}, 3000);
            }}

            login("{token}");
            """
        )

        sleep(30)


def init_discord_robot() -> DiscordRobot:
    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_experimental_option("useAutomationExtension", False)

    service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    return DiscordRobot(driver)
