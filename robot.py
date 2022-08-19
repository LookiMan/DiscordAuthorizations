from urllib.parse import parse_qs
from json import loads
from time import sleep

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By

from twocaptcha import TwoCaptcha

from config import CAPTCHA_API_TOKEN


CHROMEDRIVER_PATH = "./src/chromedriver.exe"


class DiscordRobot(object):
    def __init__(self, wd, solver):
        self.wd = wd
        self.solver = solver

    def close(self):
        self.wd.quit()

    def start(self, credentials):
        self.open_tab("https://discord.com/register")
        self.fill_the_form(credentials)
        self.submit_form()
        self.resolve_captcha()

        time.sleep(20)

        self.close_tab()

    def await_element_to_be_clickable(self, css_selector, timeout=10):
        wait = WebDriverWait(self.wd, timeout)
        try:
            wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, css_selector)))
        except:
            raise BaseException(
                f"Element with css selector: '{css_selector}' not found!"
            )

    def open_tab(self, url):
        self.wd.get(url)

    def close_tab(self):
        self.wd.close()

    def login(self, credentials):
        self.open_tab("https://discord.com/login")

        self.await_element_to_be_clickable("")

        self.wd.find_element(By.CSS_SELECTOR, 'form input[name="email"]').send_keys(
            credentials.email
        )
        self.wd.find_element(By.CSS_SELECTOR, 'form input[name="password"]').send_keys(
            credentials.password
        )
        self.wd.execute_script(
            """
            const payload = {
                "login": document.querySelector('input[name="email"]').value,
                "password": document.querySelector('input[name="password"]').value,
                "undelete": false,
                "captcha_key": null,
                "gift_code_sku_id": null,
                "login_source": null,
            }

            var xhr = new XMLHttpRequest();
            xhr.open("POST", "https://discord.com/api/v9/auth/login");
            xhr.setRequestHeader('Content-type', 'application/json; charset=utf-8');

            xhr.onreadystatechange = function() {
                if (this.readyState === 4){
                    const input = document.createElement("input");
                    input.setAttribute("id", "user-token");               
                    input.setAttribute("type", "hidden");
                    input.setAttribute("value", this.response);
                    console.log(this.response);
                    document.body.appendChild(input);
                }
            }
            xhr.send(JSON.stringify(payload));
        """
        )

        sleep(5)

        self.response = self.wd.execute_script(
            "return document.querySelector('#user-token').value;"
        )

        token = loads(self.response).get("token")

        self.wd.find_element(By.CSS_SELECTOR, 'form button[type="submit"]').click()

        return token

    def fill_the_form(self, credentials):
        self.wd.find_element(By.CSS_SELECTOR, 'form input[type="email"]').send_keys(
            credentials.email
        )
        self.wd.find_element(By.CSS_SELECTOR, 'form input[type="text"]').send_keys(
            credentials.username
        )

        self.wd.find_element(By.CSS_SELECTOR, 'form input[type="password"]').send_keys(
            credentials.password
        )

        self.select_day()
        self.select_month()
        self.insert_year("1999")

    def select_day(self):
        selector = "#react-select-2-option-0"

        self.wd.find_element(By.CSS_SELECTOR, 'div[tabindex="1"]').click()

        self.await_element_to_be_clickable(selector)
        self.wd.find_element(By.CSS_SELECTOR, selector).click()

    def select_month(self):
        selector = "#react-select-3-option-0"

        self.wd.find_element(By.CSS_SELECTOR, 'div[tabindex="2"]').click()
        self.await_element_to_be_clickable(selector)

        self.wd.find_element(By.CSS_SELECTOR, selector).click()

    def insert_year(self, year: str):
        self.wd.find_element(By.CSS_SELECTOR, "#react-select-4-input").send_keys(year)

    def submit_form(self):
        self.wd.find_element(By.CSS_SELECTOR, 'form button[type="submit"]').click()

    def resolve_captcha(self):
        # self.await_element_to_be_clickable("iframe")
        sleep(2)

        self.url = self.wd.execute_script(
            """
            return document.getElementsByTagName('iframe')[0].getAttribute("src");
            """
        )

        result = self.solver.hcaptcha(
            sitekey=parse_qs(self.url)["sitekey"][0],
            url=self.wd.current_url,
        )

        if result:
            code = result.get("code", "")

            self.wd.execute_script(
                f'document.querySelector(\'textarea[name="h-recaptcha-response"]\').innerHTML = "{code}";'
            )

        self.wd.find_element(By.CSS_SELECTOR, "no-selection").click()
        self.await_element_to_be_clickable(".button-submit")
        self.wd.find_element(By.CSS_SELECTOR, ".button-submit").click()


def init_discord_robot():
    solver = TwoCaptcha(CAPTCHA_API_TOKEN)

    options = webdriver.ChromeOptions()
    options.add_argument("no-sandbox")
    options.add_experimental_option("useAutomationExtension", False)

    service = ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=service, options=options)

    return DiscordRobot(driver, solver)
