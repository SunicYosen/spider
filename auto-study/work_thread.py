import os
import sys
import json

from PyQt5.QtCore import QThread, pyqtSignal

from init_chromedriver import init_chromedriver
from login import login_study, check_login, get_qrcode_screen_pic
from get_user_name import get_user_name
from read_articles import read_articles
from watch_videos import watch_videos
from daily_exam import daily_exam
from weekly_exam import weekly_exam
from special_exam import special_exam
from get_scores import get_scores

class WorkThread(QThread):
    home_url     = "https://www.xuexi.cn/"
    login_url    = "https://pc.xuexi.cn/points/login.html"
    exam_url     = 'https://pc.xuexi.cn/points/exam-index.html'
    score_url    = 'https://pc.xuexi.cn/points/my-points.html'
    signal       = pyqtSignal(str)
    login_signal = pyqtSignal(bool)
    login_qrcode = pyqtSignal(str)
    signal_score = pyqtSignal(list)
    is_driverd   = False

    def __init__(self, args):
        super(WorkThread, self).__init__()
        self.redirect_stdout()
        self.cookies  = []
        self.args     = args
        self.is_login = False
        self.load_cookie()
        self.init_dirver()

    def redirect_stdout(self):
        self.stdoutbak = sys.stdout
        self.stderrbak = sys.stderr
        sys.stdout = self

    def write(self, info):
        self.signal.emit(info)

    def load_cookie(self):
        self.cookie_path = os.path.join(os.path.dirname(__file__), self.args.cookie)
        if os.path.exists(self.cookie_path):
            try:
                with open(self.cookie_path) as cookie_file:
                    data = json.load(cookie_file)
                    self.cookies = data['cookie']
            except:
                self.signal.emit("[+]: Load cookie: {} Failed！".format(self.cookie_path))

    def update_cookie(self):
        self.cookies = self.driver.get_cookies()

    def save_cookies(self):
        with open(self.cookie_path, 'w') as f:
            json.dump({'cookie': list(self.cookies)}, f)

    def init_dirver(self):
        self.driver = init_chromedriver(self.args.chrome, cookies=self.cookies)
        self.is_driverd = True
    
    def login(self):
        while check_login(self.driver, self.login_url, self.cookies):
            self.qrcode_path = get_qrcode_screen_pic(self.driver, self.login_url)
            self.login_qrcode.emit(self.qrcode_path)
            login_study(self.driver)
        self.name = get_user_name(self.driver, self.exam_url)
        self.is_login = True
        self.login_signal.emit(True)
        self.update_cookie()
        self.save_cookies()

    def read_articles(self):
        if self.is_login:
            read_articles(self.driver, read_mode=1)
            self.update_cookie()
            self.save_cookies()
        else:
            self.signal.emit("[-]: Error Read Articles. Please Login First!")

    def watch_videos(self):
        if self.is_login:
            watch_videos(self.driver)
            self.update_cookie()
            self.save_cookies()
        else:
            self.signal.emit("[-]: Error Watch Videos. Please Login First!")

    def daily_exam(self):
        if self.is_login:
            daily_exam(self.driver, self.exam_url)
            self.update_cookie()
            self.save_cookies()
        else:
            self.signal.emit("[-]: Error Daily Exam. Please Login First!")

    def weekly_exam(self):
        if self.is_login:
            weekly_exam(self.driver, self.exam_url)
            self.update_cookie()
            self.save_cookies()
        else:
            self.signal.emit("[-]: Error Weekly Exam. Please Login First!")

    def special_exam(self):
        if self.is_login:
            special_exam(self.driver, self.exam_url)
            self.update_cookie()
            self.save_cookies()
        else:
            self.signal.emit("[-]: Error Special Exam. Please Login First!")

    def get_scores(self):
        if self.is_login:
            score_list, score_titles = get_scores(self.driver, self.score_url)
            self.signal_score.emit([score_list, score_titles])
            self.update_cookie()
            self.save_cookies()
        else:
            self.signal.emit("[-]: Error Get Scores. Please Login First!")

    def run(self):
        if "l" in self.args:
            self.login()
        if "r" in self.args:
            self.read_articles()
        if "w" in self.args:
            self.watch_videos()
        if "d" in self.args:
            self.daily_exam()
        if "x" in self.args:
            self.weekly_exam()
        if "v" in self.args:
            self.special_exam()
        if "s" in self.args:
            self.get_scores()
        self.signal.emit("\n")
