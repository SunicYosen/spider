import os
import sys

from PIL import Image
from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QApplication, qApp, QGraphicsPixmapItem, QGraphicsScene
from PyQt5.QtCore import QEventLoop, QCoreApplication

from args_parser import args_sparse
from work_thread import WorkThread

class AutoStudyGui(QWidget):

    def __init__(self, args):
        super(AutoStudyGui, self).__init__()
        self.args     = args
        self.is_login = False
        self.load_ui('auto_study.ui')
        self.xuexi_pic_path = "xuexi.jpg"
        self.work_thread = WorkThread(self.args)
        self.work_thread.signal.connect(self.write)
        self.work_thread.login_signal.connect(self.set_login)
        self.work_thread.login_qrcode.connect(self.set_qrcode)
        self.work_thread.signal_score.connect(self.set_score)
        self.set_login(False)
        self.login_bt_action()
        self.read_articles_bt_action()
        self.watch_videos_bt_action()
        self.daily_exam_bt_action()
        self.weekly_exam_bt_action()
        self.special_exam_bt_action()
        self.get_scores_bt_action()
        self.quit_bt_action()
        # self.init_driver()

    def load_ui(self, ui_path=''):
        uic.loadUi(ui_path,self)

    def write(self, info):
        self.log_browser.insertPlainText(info)
        qApp.processEvents(QEventLoop.ExcludeUserInputEvents | QEventLoop.ExcludeSocketNotifiers)
        # self.stdoutbak.write(info)

    def set_login(self, flag):
        if flag:
            self.user_broswer.setText("已登录")
            self.label.setText("已登录，欢迎学习！")
            pix   = QPixmap()
            pix.load(self.xuexi_pic_path)
            item  = QGraphicsPixmapItem(pix)
            scene = QGraphicsScene()
            scene.addItem(item)
            self.qrcode_viewer.setScene(scene)
        else:
            self.user_broswer.setText("未登录")

    def set_qrcode(self, qrcode_path):
        if os.path.exists(qrcode_path):
            pix   = QPixmap()
            pix.load(qrcode_path)
            item  = QGraphicsPixmapItem(pix)
            scene = QGraphicsScene()
            scene.addItem(item)
            self.qrcode_viewer.setScene(scene)

    def set_score(self, score_list):
        self.score_broswer.setText(str(score_list[1])+"/"+str(score_list[0]))

    def login_bt_action(self):
        self.login_bt.clicked[bool].connect(self.login_start)

    def login_start(self):
        self.work_thread.args = ["l"]
        self.work_thread.start()

    def read_articles_bt_action(self):
        self.read_article_bt.clicked[bool].connect(self.read_articles_start)

    def read_articles_start(self):
        self.work_thread.args = ["r"]
        self.work_thread.start()

    def watch_videos_bt_action(self):
        self.watch_videos_bt.clicked[bool].connect(self.watch_videos_start)

    def watch_videos_start(self):
        self.work_thread.args = ["w"]
        self.work_thread.start()

    def daily_exam_bt_action(self):
        self.daily_exam_bt.clicked[bool].connect(self.daily_exam_start)

    def daily_exam_start(self):
        self.work_thread.args = ["d"]
        self.work_thread.start()

    def weekly_exam_bt_action(self):
        self.weekly_exam_bt.clicked[bool].connect(self.weekly_exam_start)

    def weekly_exam_start(self):
        self.work_thread.args = ["x"]
        self.work_thread.start()

    def special_exam_bt_action(self):
        self.special_exam_bt.clicked[bool].connect(self.special_exam_start)

    def special_exam_start(self):
        self.work_thread.args = ["v"]
        self.work_thread.start()

    def get_scores_bt_action(self):
        self.get_scores_bt.clicked[bool].connect(self.get_scores_start)

    def get_scores_start(self):
        self.work_thread.args = ["s"]
        self.work_thread.start()

    def do_all_bt_action(self):
        self.do_all_bt.clicked[bool].connect(self.do_all_start)

    def do_all_start(self):
        self.work_thread.args = ["l","r","w","d","x","v","s"]
        self.work_thread.start()

    def quit_bt_action(self):
        self.quit_bt.clicked[bool].connect(self.quit_bt_start)

    def quit_bt_start(self):
        self.work_thread.driver.quit()
        QCoreApplication.quit()

def main():
    args   = args_sparse()
    app    = QApplication(sys.argv)
    window = AutoStudyGui(args)
    window.setWindowTitle("Auto Study")
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()