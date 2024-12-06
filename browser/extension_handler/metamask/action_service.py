import re
import time

from loguru import logger
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC

from browser.pages import BasePage


class MetamaskActionsService(BasePage):
    PASSWORD_FIELD = "#password-label"
    UNLOCK_WALLET = "[data-testid='unlock-submit']"
    NEXT_BUTTON = "[data-testid='page-container-footer-next']"
    CONFIRMATION_SUBMIT_BITTON = "[data-testid='confirmation-submit-button']"
    CLOSE_ADD_BUTTON = "[data-testid='popover-close']"
    ADD_NETWORK_MANUALLY_BUTTON = "[data-testid='add-network-manually']"
    NETWORK_INTO_FIELD = ".form-field"
    CURRENCY_SYMBOL_FIELD = "[data-testid='network-form-ticker-input']"
    SENDING_BUTTON = "[data-testid='eth-overview-send']"
    GOT_IT_LOCATOR = "//p[@data-testid='multichain-product-tour-menu-popover-step-counter']/..//button"

    def __init__(self, driver: WebDriver, metamask_url: str = None):
        super().__init__(driver)
        self.driver = driver
        self.metamask_url = metamask_url
        self._metamask_page = None

    # def get_address(self, wallet_seed_phrase: str):
    #     # Method to generate Ethereum address from seed phrase using Web3
    #     derivation_path_metamask = "/44'/60'/0'/0"
    #     wallet = Wallet(wallet_seed_phrase, None, derivation_path_metamask)
    #     account = wallet.get_account(0)
    #     address = account.address
    #     logger.info(f"Derived Ethereum address: {address}")
    #     return address

    def get_metamask_window(self):
        time.sleep(2)  # Simulating wait as in Playwright
        try:
            # Finding the Metamask window by title (use Selenium to switch to the correct window)
            windows = self.driver.window_handles
            for window in windows:
                self.driver.switch_to.window(window)
                if "Metamask" in self.driver.title:
                    self._metamask_page = self.driver
                    self.driver.switch_to.window(window)
                    self.driver.get(self.metamask_url)
                    return self._metamask_page
        except Exception as e:
            logger.error(f"Error finding Metamask window: {e}")
            raise Exception("Metamask window not found")

    def get_available_selector(self):
        if self.is_element_visible(self.CONFIRMATION_SUBMIT_BITTON):
            return self.CONFIRMATION_SUBMIT_BITTON
        elif self.is_element_visible(self.NEXT_BUTTON):
            return self.NEXT_BUTTON
        return None

    def any_approve_transaction(self):
        while not self.is_element_visible(self.SENDING_BUTTON):
            available_selector = self.get_available_selector()
            logger.debug(f"In this page available: {available_selector}")
            if available_selector:
                self.click_element(By.CSS_SELECTOR, available_selector)
                logger.debug(f"Clicked on {available_selector}")
            time.sleep(2)

    def close_additional_add(self):
        if self.is_element_visible(self.CLOSE_ADD_BUTTON):
            self.click_element(By.CSS_SELECTOR, self.CLOSE_ADD_BUTTON)
            if self.is_element_visible(self.GOT_IT_LOCATOR):
                got_it_buttons = self.driver.find_elements(
                    By.XPATH, self.GOT_IT_LOCATOR
                )
                for button in got_it_buttons:
                    if button.is_displayed():
                        button.click()

    def login_in_metamask(self, wallet_password: str):
        self.check_available_metamask_instance_page()
        self.type_element(By.CSS_SELECTOR, self.PASSWORD_FIELD, wallet_password)
        self.click_element(By.CSS_SELECTOR, self.UNLOCK_WALLET)

    def approve_connect_metamask_to_site(self):
        self.check_available_metamask_instance_page()
        self.click_element(By.CSS_SELECTOR, self.NEXT_BUTTON)
        self.click_element(By.CSS_SELECTOR, self.NEXT_BUTTON)

    def submit_transaction_after_network_change(self):
        self.check_available_metamask_instance_page()
        self.click_element(By.CSS_SELECTOR, self.NEXT_BUTTON)

    def check_available_metamask_instance_page(self):
        try:
            body = self.find_element(By.CSS_SELECTOR, "body")
            if body.is_displayed():
                logger.info("Metamask page available")
        except Exception as ex:
            logger.error(f"Metamask page not available, trying to get a new one: {ex}")
            self.get_metamask_window()

    def change_network_in_transaction(self):
        self.check_available_metamask_instance_page()
        self.click_element(By.CSS_SELECTOR, self.CONFIRMATION_SUBMIT_BITTON)

    def add_another_network(self, network_model):
        self.metamask_url = re.sub(r"#.*", "#", self.metamask_url)
        configs_url = f"{self.metamask_url}settings/networks/add-popular-custom-network"
        self.navigate(configs_url)

        self.wait_for_element(self.ADD_NETWORK_MANUALLY_BUTTON)
        self.click_element(By.CSS_SELECTOR, self.ADD_NETWORK_MANUALLY_BUTTON)

        field_selectors = self.driver.find_elements(
            By.CSS_SELECTOR, self.NETWORK_INTO_FIELD
        )
        field_selectors[0].click()
        field_selectors[0].send_keys(network_model["NetworkName"])
        field_selectors[1].click()
        field_selectors[1].send_keys(network_model["UrlNetwork"])
        field_selectors[2].click()
        field_selectors[2].send_keys(network_model["ChainId"])

        self.click_element(By.CSS_SELECTOR, self.CURRENCY_SYMBOL_FIELD)
        self.type_element(
            By.CSS_SELECTOR, self.CURRENCY_SYMBOL_FIELD, network_model["CurrencySymbol"]
        )

        buttons = self.driver.find_elements(By.CSS_SELECTOR, self.buttons)
        buttons[1].click()

        result = self.is_element_visible(self.NETWORK_ADD_SUCCESSFUL)
        logger.info(f"Network adding result: {result}")

    def is_element_visible(self, selector):
        try:
            element = self.driver.find_element(By.CSS_SELECTOR, selector)
            return element.is_displayed()
        except:
            return False

    def wait_for_element(self, selector, timeout=10):
        WebDriverWait(self.driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    def type_element(self, by: By, value: str, text: str):
        element = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((by, value))
        )
        element.clear()
        element.send_keys(text)
