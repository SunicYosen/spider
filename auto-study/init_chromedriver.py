'''

'''
import time
import platform
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from get_usr_data_dir import get_usr_data_dir

class SafeChrome:
    def __init__(self, show_flag=False):
        self.chrome_options = Options()
        if not show_flag:
            self.chrome_options.add_argument('--headless')
        # self.chrome_options.add_argument('--no-sandbox')
        # self.chrome_options.add_argument('--disable-dev-shm-usage')
        user_data_path = get_usr_data_dir()
        self.chrome_options.add_argument(user_data_path)

        if platform.system().lower() == 'linux':
            self.driver = webdriver.Chrome(options=self.chrome_options)
        elif platform.system().lower() == 'windows':
            self.driver = webdriver.Chrome('./tools/win32/chromedriver.exe', options=self.chrome_options)
        else:
            print('[-] ', str(platform.system()), 'not supported!')
            exit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()

    def __del__(self):
        if self.driver:
            self.driver.quit()

def init_chromedriver(show_flag=False):
    safe_chrome = SafeChrome(show_flag)
    return safe_chrome.driver

def main():
    show_flag = True
    driver = init_chromedriver(show_flag)
    time.sleep(1)
    driver.quit()

if __name__ == '__main__':
    main()