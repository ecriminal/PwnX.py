import validators
import requests


class Validate:

    @staticmethod
    def url(url):
        return validators.url(url)

    @staticmethod
    def active_url(url, timeout=2500):
        try:
            requests.get(url, timeout=timeout / 1000)
            return True
        except Exception:
            return False
