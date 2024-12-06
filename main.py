import time

from loguru import logger

from browser.proxy import ProxyManager
from browser.manager import WebDriverManager
from browser.session import SessionManager


def main():
    proxy_list = []
    metamask_path = "extensions/MetaMask-Chrome"
    webrtc_path = "extensions/WebRTC-Leak-Prevent-Chrome"

    logger.info(f"WebRTC path: {metamask_path}")
    proxy_manager = ProxyManager(proxy_list) if proxy_list else None
    webdriver_manager = WebDriverManager(
        metamask_path=metamask_path,
        webrtc_path=webrtc_path,
    )
    session_manager = SessionManager(webdriver_manager, proxy_manager)

    try:
        url = "https://app.spotlightprotocol.com/be-spotlighted"
        session_manager.start_session(url)
        print("Navigation successful")
        time.sleep(60)
    finally:
        session_manager.end_session()
        print("Session ended")


if __name__ == "__main__":
    main()
