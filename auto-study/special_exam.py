
import time
import difflib

from do_exam import do_exam

def get_special_list_page(driver):
    try:
        driver.find_elements_by_class_name("block")[2].click()
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)

    except:
        print("[-]: Get Exam Weekly List Page Failed!")
        exit()

def get_special_last(driver):
    special_list = driver.find_elements_by_tag_name("button")

    for special in special_list:
        if (special.get_attribute("innerText") == "开始答题") or (special.get_attribute("innerText") == "继续答题") or (special.get_attribute("innerText") == "重新答题"):
            special.click()
            time.sleep(1)
            break

def special_exam(driver, url='https://pc.xuexi.cn/points/exam-index.html', special_num=1, questions_per_special=10):
    print("[+]: Do Special Exam - ", special_num, "Special(s)", questions_per_special, "Question(s) per Special.")
    driver.get(url)
    get_special_list_page(driver)
    get_special_last(driver)
    do_exam(driver, groups_num=special_num, questions_per_group=questions_per_special)
    print("[+]: 完成专题答题！")