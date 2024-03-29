
import time
import difflib

from do_exam import do_exam

def get_daily_practice_page(driver):
    try:
        driver.find_elements_by_class_name("block")[0].click()
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
    except:
        print("[-]: Get Exam Practice Page Failed!")
        exit()

def daily_exam(driver, url='https://pc.xuexi.cn/points/exam-index.html', questions_per_group=5):
    print("[+]: Do Daily Exam - ", questions_per_group, "Question(s) per Group.")
    try:
        driver.get(url)
    except:
        print("[-]: Daily Exam Failed! Get Exam Page Error!")
        return
    
    time.sleep(1)
    get_daily_practice_page(driver)
    do_exam(driver)
    print("[+]: 完成每日答题！")