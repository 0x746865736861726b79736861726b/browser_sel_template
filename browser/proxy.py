import random


class ProxyManager:
    def __init__(self, proxy_list):
        self.proxy_list = proxy_list

    def get_random_proxy(self):
        return random.choice(self.proxy_list)
