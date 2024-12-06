from loguru import logger

from selenium.webdriver.common.by import By

from .base_page import BasePage


class SpotlightPage(BasePage):
    LOGIN_BUTTON_XPATH = "//button[contains(text(), 'Connect')]"
    METAMASK_BUTTON_XPATH = "//div[contains(text(), 'MetaMask')]"
    NAME_SPOTLIGHT = "//input[@id='name']"
    DESCRIPTION_SPOTLIGHT = "//input[@id='description']"
    MINT_SPOTLIGHT = "//button[text()='Mint Now']"

    def __init__(self, driver):
        self.driver = driver

    def navigate(self, url):
        self.driver.get(url)

    def login(self):
        self.click_element(By.XPATH, self.LOGIN_BUTTON_XPATH)
        self.click_element(By.XPATH, self.METAMASK_BUTTON_XPATH)

    def get_login_status(self):
        return self.driver.find_element(By.ID, "status").text

    def fill_details_spotlight(self, name, description):
        try:
            self.click_element(By.XPATH, self.NAME_SPOTLIGHT)
            self.type_text(By.XPATH, self.NAME_SPOTLIGHT, name)

            self.click_element(By.XPATH, self.DESCRIPTION_SPOTLIGHT)
            self.type_text(By.XPATH, self.DESCRIPTION_SPOTLIGHT, description)
            self.click_element(By.XPATH, self.MINT_SPOTLIGHT)
        except Exception as e:
            logger.error(f"Error filling details: {e}")
            raise
