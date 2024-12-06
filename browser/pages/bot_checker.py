import time

from seleniumbase import BaseCase
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BotCheckerPage(BaseCase):
    CHECK_BOX_XPATH = "//input[@id='checkbox']"

    def __init__(self, driver):
        self.driver = driver

    def navigate(self, url):
        self.driver.get(url)
        time.sleep(5)

    def click_checkbox(self):
        checkbox = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, self.CHECK_BOX_XPATH))
        )
        checkbox.click()
