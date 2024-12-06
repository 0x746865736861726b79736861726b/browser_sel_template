import os

from loguru import logger
import undetected_chromedriver as uc
from fake_useragent import UserAgent


class WebDriverManager:
    def __init__(
        self,
        proxy: str = None,
        metamask_path: str = None,
        webrtc_path: str = None,
    ):
        self.driver = None
        self.proxy = proxy
        self.metamask_path = metamask_path
        self.webrtc_path = webrtc_path

    def init_driver(self, proxy=None):
        if proxy:
            self.proxy = proxy
        options = uc.ChromeOptions()

        options.add_argument("--enable-webgl")
        options.add_argument("--use-gl=desktop")
        options.add_argument("--enable-accelerated-2d-canvas")
        options.add_argument("--enable-gpu-rasterization")
        options.add_argument("--ignore-gpu-blocklist")
        options.add_argument("--enable-webgl-draft-extensions")

        if self.metamask_path and os.path.exists(self.metamask_path):
            logger.info(f"Adding extension from {self.metamask_path}")
            options.add_argument("--load-extension=" + self.metamask_path)
        else:
            logger.info("MetaMask extension not found!")

        # if self.webrtc_path and os.path.exists(self.webrtc_path):
        #     logger.info(f"Adding extension from {self.webrtc_path}")
        #     options.add_argument("--load-extension=" + self.webrtc_path)
        # else:
        #     logger.info("WebRTC extension not found!")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-popup-blocking")
        options.add_argument(f"user-agent={UserAgent().chrome}")
        options.add_argument("--disable-site-isolation-trials")
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_argument("--disable-features=RendererCodeIntegrity")
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-features=IsolateOrigins,site-per-process")
        # Initialize the driver
        self.driver = uc.Chrome(options=options)
        self.driver.execute_script(
            "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
        )
        self.driver.execute_cdp_cmd(
            "Network.setUserAgentOverride",
            {
                "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/83.0.4103.53 Safari/537.36"
            },
        )

        # Debug WebGL Context
        webgl_status = self.check_webgl()
        logger.info(f"WebGL Status: {webgl_status}")
        screenshot_path = self.take_screenshot("browser_screenshot.png")
        logger.info(f"Screenshot saved to {screenshot_path}")
        return self.driver

    def check_webgl(self):
        if self.driver:
            webgl_context = """
            const canvas = document.createElement('canvas');
            const gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');
            return gl ? 'WebGL Supported' : 'WebGL Not Supported';
            """
            return self.driver.execute_script(webgl_context)

    def take_screenshot(self, filename: str):
        if self.driver:
            os.makedirs("screenshots", exist_ok=True)
            filepath = os.path.join("screenshots", filename)
            self.driver.save_screenshot(filepath)
            return filepath

    def quit_driver(self):
        if self.driver:
            self.driver.quit()
