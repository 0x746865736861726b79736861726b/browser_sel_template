from .base_page import BasePage


class TwitterPage(BasePage):
    def __init__(self, driver):
        self.driver = driver

    def navigate(self, auth_token: str):
        self.driver.get("https://x.com/")
        cookie = {
            "name": "auth_token",
            "value": "309e050855bda8c93072e03915d9a0e6dc109b8a",
            "domain": ".x.com",
            "path": "/",
            "secure": True,
            "httpOnly": True,
        }
        self.driver.add_cookie(cookie)
        self.driver.get("https://x.com/home")
