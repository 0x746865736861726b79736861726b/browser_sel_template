from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver: WebDriver):
        self.driver = driver

    def navigate(self, url: str):
        self.driver.get(url)

    def find_element(self, by: By, value: str, timeout: int = 10):
        return WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((by, value))
        )

    def click_element(self, by: By, value: str, timeout: int = 30):
        element = WebDriverWait(self.driver, timeout).until(
            EC.element_to_be_clickable((by, value))
        )
        element.click()
        return element

    def type_text(self, by: By, value: str, text: str, timeout: int = 10):
        element = self.find_element(by, value, timeout)
        element.send_keys(text)
