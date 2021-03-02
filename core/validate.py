import validators
import requests


class Validate:

    @staticmethod
    def url(url):
        """ Validate URL """
        return validators.url(url)

    @staticmethod
    def active_url(url, timeout=2500):
        """ Check if web site is reachable """
        try:
            requests.get(url, timeout=timeout / 1000)
            return True
        except Exception:
            return False
