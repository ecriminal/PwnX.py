class Banner:

    __BANNER = '''
 _____           __ __ 
|  _  |_ _ _ ___|  |  |    Misconfigured ShareX API RCE
|   __| | | |   |-   -|    Developed by cs
|__|  |_____|_|_|__|__|.py\n
'''[1:-1]

    @staticmethod
    def print():
        print(Banner.__BANNER)
