'''
return chrome usr data path
'''

import platform

def get_usr_data_dir():
    if platform.system().lower() == 'windows':
        return "--user-data-dir=C:\\Users\\17482\\AppData\\Local\\Google\\Chrome\\User Data1"
    elif platform.system().lower() == 'linux':
        return "--user-data-dir=/home/sun/.config/google-chrome/Default"

if __name__ == "__main__":
    print(get_usr_data_dir())