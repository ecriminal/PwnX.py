import datetime
import json
import os


class Cache:

    path = os.path.join('cache', 'shells.json')

    @staticmethod
    def __read():
        """ Read from cache """
        with open(Cache.path, 'r') as f:
            cache_content = f.read()
        return json.loads(cache_content)

    @staticmethod
    def __write(cache_content):
        """ Write to cache """
        with open(Cache.path, 'w') as f:
            f.write(json.dumps(cache_content))

    @staticmethod
    def __init():
        """ Initialize cache """
        if not os.path.exists(os.path.dirname(Cache.path)):
            os.mkdir('cache', 660)

        if not os.path.exists(Cache.path) or not os.path.isfile(Cache.path):
            Cache.flush()

        # validates JSON object in data.json file
        # and clears cache if JSON object in cache file is invalid
        try:
            Cache.__read()
        except Exception:
            Cache.flush()

    @staticmethod
    def save(upload_url, shell_url):
        """ Save shell URL to cache """
        target = [x for x in upload_url.split('/') if len(x) > 0][1]

        Cache.__init()

        cache_data = {
            'date': datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'target': target,
            'upload_url': upload_url,
            'shell_url': shell_url
        }

        cache_content = Cache.__read()
        cache_content.append(cache_data)

        Cache.__write(cache_content)

    @staticmethod
    def get(url):
        """ Fetch shell URL from cache """
        target = [x for x in url.split('/') if len(x) > 0][1]

        Cache.__init()

        cache_content = Cache.__read()

        for elem in cache_content:
            if elem['target'].lower() == target:
                return elem

        return None

    @staticmethod
    def flush():
        """ Clear cache """
        Cache.__write([])
