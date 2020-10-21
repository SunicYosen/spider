
import sys
import platform
from selenium import webdriver

from PyQt5.QtCore import QThread, pyqtSignal

from get_usr_data_dir import get_usr_data_dir
from login import login_study, check_login, get_qrcode_screen_pic
from read_articles import read_articles
from watch_videos import watch_videos
from daily_exam import daily_exam
from weekly_exam import weekly_exam
from special_exam import special_exam
from get_scores import get_scores

class WorkThread(QThread):
    home_url     = "https://www.xuexi.cn/"
    login_url    = "https://pc.xuexi.cn/points/login.html"
    article_urls = ["https://www.xuexi.cn/xxqg.html?id=36a1bf1b683942fe917fc1866f13fc21","https://www.xuexi.cn/xxqg.html?id=2813415f8e1c48b4b47e794aca7b7bb5"]
    videos_url   = 'https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html'
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
        if args.chrome:
            self.args = ["c"]
        else:
            self.args = []
        self.is_login = False
        self.init_dirver()

    def redirect_stdout(self):
        self.stdoutbak = sys.stdout
        self.stderrbak = sys.stderr
        sys.stdout = self

    def write(self, info):
        self.signal.emit(info)

    def init_dirver(self):
        chrome_options = webdriver.ChromeOptions()

        # chrome_options.add_argument('--headless')
        if "c" in self.args:
            pass
        else:
            chrome_options.add_argument('--headless')
        user_data_path = get_usr_data_dir()
        chrome_options.add_argument(user_data_path)

        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')

        if platform.system().lower() == 'linux':
            self.driver = webdriver.Chrome(options=chrome_options)
        else:
            self.driver = webdriver.Chrome('./tools/win32/chromedriver.exe', options=chrome_options)

        self.is_driverd = True
    
    def login(self):
        while check_login(self.driver, self.login_url):
            self.qrcode_path = get_qrcode_screen_pic(self.driver, self.login_url)
            self.login_qrcode.emit(self.qrcode_path)
            login_study(self.driver)
        self.is_login = True
        self.login_signal.emit(True)

    def read_articles(self):
        if self.is_login:
            read_articles(self.driver, self.article_urls)
        else:
            self.signal.emit("[-]: Error Read Articles. Please Login First!")

    def watch_videos(self):
        if self.is_login:
            watch_videos(self.driver, self.videos_url)
        else:
            self.signal.emit("[-]: Error Read Articles. Please Login First!")

    def daily_exam(self):
        if self.is_login:
            daily_exam(self.driver, self.exam_url)
        else:
            self.signal.emit("[-]: Error Read Articles. Please Login First!")

    def weekly_exam(self):
        if self.is_login:
            weekly_exam(self.driver, self.exam_url)
        else:
            self.signal.emit("[-]: Error Read Articles. Please Login First!")

    def special_exam(self):
        if self.is_login:
            special_exam(self.driver, self.exam_url)
        else:
            self.signal.emit("[-]: Error Read Articles. Please Login First!")

    def get_scores(self):
        if self.is_login:
            total_score, today_score = get_scores(self.driver, self.score_url)
            self.signal_score.emit([total_score, today_score])
        else:
            self.signal.emit("[-]: Error Read Articles. Please Login First!")

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
