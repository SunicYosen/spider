"""""""""""""""""""""
Chrome User Data Path
"""""""""""""""""""""

import platform

def get_usr_data_dir():
    if platform.system().lower() == 'windows':
        return "--user-data-dir=C:\\Users\\Sun\\AppData\\Local\\Google\\Chrome\\User Data"
    elif platform.system().lower() == 'linux':
        return "--user-data-dir=/home/sun/.config/google-chrome/Default"

if __name__ == "__main__":
    print(get_usr_data_dir())