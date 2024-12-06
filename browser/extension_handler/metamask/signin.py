import time
from loguru import logger

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from browser.pages import BasePage


class SingInMetamaskPage(BasePage):
    ON_BOARDING = "['data-testid='onboarding-welcome']"
    AGREE_TERMS = (
        "//input[@type='checkbox' and @data-testid='onboarding-terms-checkbox']"
    )
    IMPORT_WALLET_BUTTON = "[data-testid='onboarding-import-wallet']"
    PASSWORD_INPUT_FIELD = ".form-field__input"
    CONFIRM_PHRASE_BUTTON = "[data-testid='import-srp-confirm']"
    DONE_BUTTON = "[data-testid='pin-extension-done']"
    GOT_IT_BUTTON = "[data-testid='onboarding-complete-done']"
    IMPORT_EXISTING_WALLET = "[data-testid='onboarding-import-wallet']"
    WORD_FIELD = "#import-srp__srp-word-"

    def __init__(self, driver: WebDriver):
        super().__init__(driver)
        self.metamask_url = (
            "chrome-extension://kpndmealhmhadkpebbncnkcgpngjpheo/home.html"
        )

    def get_available_selector(self):
        if self.is_element_visible(self.GOT_IT_BUTTON):
            return self.GOT_IT_BUTTON
        if self.is_element_visible(self.DONE_BUTTON):
            return self.DONE_BUTTON
        return None

    def is_element_visible(self, selector: str):
        try:
            self.find_element(By.CSS_SELECTOR, selector, timeout=5)
            return True
        except:
            return False

    def setup_in_metamask(self, seed_phrase: str):
        word_list = seed_phrase.split(" ")

        self.navigate(self.metamask_url)
        time.sleep(10)
        logger.info(f"Metamask url: {self.metamask_url}")
        try:  # self.click_element(By.CSS_SELECTOR, self.GOT_IT_BUTTON)

            self.click_element(By.XPATH, self.AGREE_TERMS)
            self.click_element(By.CSS_SELECTOR, self.IMPORT_WALLET_BUTTON)
        except Exception as e:
            logger.error(f"Error filling details: {e}")

        for index, word in enumerate(word_list):
            field_selector = f"{self.WORD_FIELD}{index}"
            self.type_text(By.CSS_SELECTOR, field_selector, word)

        self.click_element(By.CSS_SELECTOR, self.CONFIRM_PHRASE_BUTTON)

        self.type_text(By.CSS_SELECTOR, self.PASSWORD_INPUT_FIELD, "S0m3P4s5w0rd")

        self.click_element(By.CSS_SELECTOR, self.import_wallet_button)

        time.sleep(4)

        while not self.is_element_visible(self.DONE_BUTTON):
            available_selector = self.get_available_selector()
            if available_selector:
                self.click_element(By.CSS_SELECTOR, available_selector)

        self.click_element(By.CSS_SELECTOR, self.DONE_BUTTON)
        time.sleep(1)

        return self.driver

    def login_in_metamask(self, wallet_password: str):
        self.type_text(By.CSS_SELECTOR, "#password-label", wallet_password)
        self.click_element(By.CSS_SELECTOR, "[data-testid='unlock-submit']")

    def switch_to_metamask_tab(self):
        all_windows = self.driver.window_handles
        logger.info(f"Всі вкладки: {all_windows}")
        for window in all_windows:
            self.driver.switch_to.window(window)
            if self.metamask_url in self.driver.current_url:
                logger.info(
                    f"Перемикаємося на вкладку MetaMask: {self.driver.current_url}"
                )
                return

        logger.error("Вкладка MetaMask не знайдена.")
