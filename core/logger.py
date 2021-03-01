import sys


class Logger:

    @staticmethod
    def __log(prefix, color, message, file=sys.stdout):
        print(f'[ {color}{prefix} \x1b[0m] {message}\x1b[0m')

    @staticmethod
    def success(message):
        Logger.__log('OKAY', '\x1b[92m', message)

    @staticmethod
    def info(message):
        Logger.__log('INFO', '\x1b[94m', message)

    @staticmethod
    def error(message, should_exit=True):
        Logger.__log('ERRO', '\x1b[91m', message, sys.stderr)

        if should_exit:
            sys.exit(1)
