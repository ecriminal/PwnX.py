import requests

from enum import Enum


class ShareX:
    class Errors(Enum):
        UPLOAD_FAILED = {
            'reason': 'webserver doesn\'t have access to the target folder, folder doesn\'t exist or file name is missing a file extension',
            'content': 'File upload failed - CHMOD/Folder doesn\'t exist?'
        }
        MISSING_POST_SECRET = {
            'reason': 'secret key POST data field is missing in the request',
            'content': 'No post data recieved'
        }
        INVALID_SECRET = {
            'reason': 'secret key is incorrect',
            'content': 'Invalid Secret Key'
        }

    @staticmethod
    def upload(url, file_data, file_name='myfile.txt', form_name='sharex', secret=None, field_name='secret'):
        files = {form_name: (file_name, file_data, 'text/plain')}

        data = {field_name: secret} if secret is not None else {}

        return requests.post(url, headers={'User-Agent': 'ShareX/13.2.1'}, files=files, data=data)
