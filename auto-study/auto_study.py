'''
    Auto Study Command Method.
'''

import time
import re
import platform
import argparse

from args_parser import args_sparse
from init_chromedriver import init_chromedriver
from login import login_study, check_login, get_qrcode_screen_pic
from read_articles import read_articles
from watch_videos import watch_videos
from daily_exam import daily_exam
from weekly_exam import weekly_exam
from special_exam import special_exam
from get_scores import get_scores

def autostudy():
    login_url    = "https://pc.xuexi.cn/points/login.html"
    exam_url     = 'https://pc.xuexi.cn/points/exam-index.html'
    score_url    = 'https://pc.xuexi.cn/points/my-points.html'

    # sparse args
    args = args_sparse()

    if args.chrome:
        show_flag=True
    else:
        show_flag=False

    driver = init_chromedriver(show_flag=show_flag)

    # Login
    if args.login:
        while check_login(driver, login_url):
            get_qrcode_screen_pic(driver, login_url)
            login_study(driver)

    else:
        while check_login(driver, login_url):
            get_qrcode_screen_pic(driver, login_url)
            login_study(driver)
        
        if args.read:
            # Read Article
            read_articles(driver)
        if args.watch:
            # Watch Videos
            watch_videos(driver)
        if args.dexam:
            # Do Daily Exam
            daily_exam(driver, url=exam_url, questions_per_group=5)
        if args.wexam:
            # Do Weekly Exam
            weekly_exam(driver, url=exam_url, questions_per_week=5)
        if args.sexam:
            # Do Special Exam
            special_exam(driver, url=exam_url, questions_per_special=10)
        if args.score:
            get_scores(driver, score_url)

        if args.all:
            read_articles(driver)
            watch_videos(driver)
            daily_exam(driver, questions_per_group=5)
            weekly_exam(driver, questions_per_week=5)
            special_exam(driver, questions_per_special=10)
            get_scores(driver, score_url)

if __name__ == '__main__':
    autostudy()
