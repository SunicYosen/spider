'''
Main function for get conv19
Author: Sunic
For:    Champagne
'''

import time
from selenium import webdriver

from get_data import get_data
from write_excel import write_excel

def main():
    url = 'https://www.zq-ai.com/#/fe/xgfybigdata'
    output_excel = 'result.xlsx'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver  = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)
    conv19_countries = get_data(driver)
    write_excel(conv19_countries, output_excel)

if __name__ == '__main__':
    main()