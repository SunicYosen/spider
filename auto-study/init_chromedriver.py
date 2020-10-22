'''

'''
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from get_usr_data_dir import get_usr_data_dir

def init_chromedriver(show_flag=False):
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    chrome_options = Options()
    if not show_flag:
        chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    user_data_path = get_usr_data_dir()
    chrome_options.add_argument(user_data_path)

    driver = webdriver.Chrome(options=chrome_options)

    return driver

def main():
    show_flag = True
    driver = init_chromedriver(show_flag)
    time.sleep(1)
    driver.quit()

if __name__ == '__main__':
    main()