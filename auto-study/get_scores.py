
'''
 Get Score
'''
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from get_usr_data_dir import get_usr_data_dir

def get_scores(driver, url):
    """获取当前积分"""
    driver.get(url)
    time.sleep(2)
    gross_score = driver.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div[2]/div[2]/span[1]").get_attribute('innerText')
    today_score = driver.find_element_by_xpath("//span[@class='my-points-points']").get_attribute('innerText')
    print("当前总积分：" + str(gross_score))
    print("今日积分：" + str(today_score))
    return gross_score,today_score

