import time

from browser.proxy import ProxyManager
from browser.manager import WebDriverManager
from browser.pages import SpotlightPage, BotCheckerPage, TwitterPage
from browser.extension_handler.metamask.signin import SingInMetamaskPage


class SessionManager:
    def __init__(
        self,
        webdriver_manager: WebDriverManager,
        proxy_manager: ProxyManager = None,
        spotlight_page: SpotlightPage = None,
        bot_checker: BotCheckerPage = None,
    ):
        self.webdriver_manager = webdriver_manager
        self.proxy_manager = proxy_manager
        self.spotlight_page = spotlight_page
        self.bot_checker_page = bot_checker

    def start_session(self, url):
        proxy = self.proxy_manager.get_random_proxy() if self.proxy_manager else None
        driver = self.webdriver_manager.init_driver(proxy)

        self.sign_in_metamask_page = SingInMetamaskPage(driver)
        time.sleep(10)
        self.sign_in_metamask_page.switch_to_metamask_tab()
        self.sign_in_metamask_page.setup_in_metamask(
            "visual account common early move dad erupt arrive off volume butter pony"
        )
        # self.twitter_page = TwitterPage(driver)
        # self.spotlight_page = SpotlightPage(driver)
        # self.bot_checker_page = BotCheckerPage(driver)
        # self.twitter_page.navigate(
        #     "ac10ab271f1f1762ff552c2fe5d23bd68aacbffbc8d2945703ef7540bbe210cb2fc3333ebdc884ae93d9c6a12f9c0241daf13e0cf8556f770d372d67788c32e8aa31fee47cfb8a8b3d85507f0a84c373"
        # )
        # self.close_other_tabs(driver)
        # Виконуємо дії на SpotlightPage
        # self.spotlight_page.navigate(url)
        # self.spotlight_page.fill_details_spotlight(name="test", description="test")
        # page.click_checkbox()
        return self.sign_in_metamask_page

    def close_other_tabs(self, driver):
        # Get the current window handle
        main_window_handle = driver.current_window_handle

        # Get all window handles
        window_handles = driver.window_handles

        # Close all tabs except the main one (Twitter)
        for handle in window_handles:
            if handle != main_window_handle:
                driver.switch_to.window(handle)
                driver.close()

        # Switch back to the main window (Twitter)
        driver.switch_to.window(main_window_handle)

    def end_session(self):
        self.webdriver_manager.quit_driver()
