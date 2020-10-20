'''
    Auto Study Command Method.
'''

import time
import re
import platform
import argparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from get_usr_data_dir import get_usr_data_dir

from args_parser import args_sparse
from login import login_study,check_login
from read_articles import read_articles
from watch_videos import watch_videos
from daily_exam import daily_exam
from weekly_exam import weekly_exam
from special_exam import special_exam
from get_scores import get_scores

def autostudy():
    home_url     = "https://www.xuexi.cn/"
    login_url    = "https://pc.xuexi.cn/points/login.html"
    article_urls = ["https://www.xuexi.cn/xxqg.html?id=36a1bf1b683942fe917fc1866f13fc21","https://www.xuexi.cn/xxqg.html?id=2813415f8e1c48b4b47e794aca7b7bb5"]
    videos_url   = 'https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html'
    exam_url     = 'https://pc.xuexi.cn/points/exam-index.html'
    score_url    = 'https://pc.xuexi.cn/points/my-points.html'

    args = args_sparse()

    chrome_options = webdriver.ChromeOptions()

    # chrome_options.add_argument('--headless')
    if args.chrome:
        pass
    else:
        chrome_options.add_argument('--headless')
    user_data_path = get_usr_data_dir()
    chrome_options.add_argument(user_data_path)

    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    if platform.system().lower() == 'linux':
        driver = webdriver.Chrome(options=chrome_options)
    else:
        driver = webdriver.Chrome('./tools/win32/chromedriver.exe',options=chrome_options)

    # driver.get(home_url)
    # driver.implicitly_wait(5)

    # Login
    if args.login:
        while check_login(driver, login_url):
            login_study(driver, login_url)

    else:
        while check_login(driver, login_url):
            login_study(driver, login_url)
        
        if args.read:
            # Read Article
            read_articles(driver, article_urls)
        if args.watch:
            # Watch Videos
            watch_videos(driver, videos_url)
        if args.dexam:
            # Do Daily Exam
            daily_exam(driver, exam_url, 1, 5)
        if args.wexam:
            # Do Weekly Exam
            weekly_exam(driver, exam_url, 1, 5)
        if args.sexam:
            # Do Special Exam
            special_exam(driver, exam_url, 1, 10)
        if args.score:
            get_scores(driver, score_url)

        if args.all:
            read_articles(driver, article_urls)
            watch_videos(driver, videos_url)
            daily_exam(driver, exam_url, 1, 5)
            weekly_exam(driver, exam_url, 1, 5)
            special_exam(driver, exam_url, 1, 10)
            get_scores(driver, score_url)

if __name__ == '__main__':
    autostudy()
