'''
  Do Exam
'''

import time
import random
import difflib
import datetime
from selenium import webdriver

from init_chromedriver import init_chromedriver

def get_my_study_page(driver):
    try:
        driver.find_elements_by_class_name("linkItem")[1].click()
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
    except:
        print("[-]: Get Study Page Failed")
        exit()

def get_exam_page(driver):
    # Find exam index
    for link in driver.find_elements_by_xpath("//*[@href]"):
        if(link.get_attribute("href") == "https://pc.xuexi.cn/points/exam-index.html"):
            link.click()
    # Switch newest window
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)

def next_practice(driver):
    try:
        if (driver.find_elements_by_tag_name("button")[0].get_attribute("innerText") == "再来一组"):
            driver.find_elements_by_tag_name("button")[0].click()
            time.sleep(1 + random.random()*2)
    except:
        print("[-]: Next Practice Failed!")
        exit()

def choose_question(driver, rough_answer_array, clicked_flag):
    choosable_array = driver.find_elements_by_class_name("choosable")

    for i in range(len(choosable_array)):
        for j in rough_answer_array:
            if difflib.SequenceMatcher(None, choosable_array[i].get_attribute("innerText")[3:], j).ratio() >= 0.8:
                choosable_array[i].click()
                clicked_flag = True
                time.sleep(1 + random.random()*2)

    # The First Default
    if (clicked_flag == False):
        choosable_array[0].click()

    time.sleep(1 + random.random()*2)
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
    driver.find_elements_by_tag_name("button")[0].click()

    time.sleep(1 + random.random()*2)

    for i in driver.find_elements_by_tag_name("button"):
        if (i.get_attribute("innerText") == "下一题"):
            i.click()
        # For Special exam
        elif (i.get_attribute("innerText") == "交 卷"):
            print("[+]: 交卷")
            i.click()
    
    time.sleep(1 + random.random()*2)

def blank_question(driver, rough_answer_array):
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("question")[0])
    blankArr = driver.find_elements_by_class_name("blank")
    for i in range(len(blankArr)):
        blankArr[i].send_keys(rough_answer_array[i])
    time.sleep(1 + random.random()*2)
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
    driver.find_elements_by_tag_name("button")[0].click()
    time.sleep(1 + random.random()*2)

def other_question(driver):
    falseArr = []

    for ans in driver.find_elements_by_class_name("false"):
        falseArr.append(ans.get_attribute("innerText"))
        # print(ans.get_attribute("innerText"))

    for item in driver.find_elements_by_class_name("q-answer"):
        try:
            falseArr.index(item.get_attribute("innerText"))
        except ValueError:
            item.click()
    driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
    driver.find_elements_by_tag_name("button")[0].click()
    time.sleep(1 + random.random()*2)

def video_question(driver):
    if (len(driver.find_elements_by_class_name("choosable")) != 0):
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("choosable")[0])
        driver.find_elements_by_class_name("choosable")[0].click()
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
        driver.find_elements_by_tag_name("button")[0].click()
        time.sleep(1 + random.random()*2)
        driver.find_elements_by_tag_name("button")[0].click()
        time.sleep(1 + random.random()*2)
    else:
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("blank")[0])
        videoBlankArr = driver.find_elements_by_class_name("blank")
        for blank in videoBlankArr:
            blank.send_keys("a")
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
        driver.find_elements_by_tag_name("button")[0].click()
        time.sleep(1 + random.random()*2)
        driver.find_elements_by_tag_name("button")[0].click()
        time.sleep(1 + random.random()*2)

def get_rough_answer(driver, rough_answer_array):
    fontArr = driver.find_elements_by_tag_name("font")
    for fontEL in fontArr:
        if (fontEL.get_attribute("innerText") != ""):
            rough_answer_array.append(fontEL.get_attribute("innerText"))

# Do exam
def do_exam(driver, groups_num=1, questions_per_group=5):
    counter            = 0
    clicked_flag       = False
    rough_answer_array = []
    random.seed(datetime.datetime.now())

    while(counter < groups_num * questions_per_group):
        counter += 1
        time.sleep(1 + random.random()*2)
        rough_answer_array.clear()

        if(counter%questions_per_group == 1):
            print("[+]: Doing Exam: Group ", int(counter/questions_per_group)+1, '/', groups_num)

        if(counter%questions_per_group == 0):
            print("[+]: -- ", questions_per_group, '/', questions_per_group)
        else:
            print("[+]: -- ", counter%questions_per_group, '/', questions_per_group)

        # If next practice
        next_practice(driver)

        if(len(driver.find_elements_by_class_name("tips")) != 0):
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("tips")[0])
            driver.find_elements_by_class_name("tips")[0].click()

            if (driver.find_elements_by_class_name("line-feed")[0].get_attribute("innerText") == "请观看视频"):
                driver.find_elements_by_class_name("tips")[0].click()
                video_question(driver)

            get_rough_answer(driver, rough_answer_array)

            time.sleep(1 + random.random()*2)
            driver.find_elements_by_class_name("tips")[0].click()
            time.sleep(1 + random.random()*2)
            # print(rough_answer_array)

        # Scroll
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("question")[0])
        time.sleep(1 + random.random()*2)

        # Get the type of questions
        if len(driver.find_elements_by_class_name("false")) != 0:
            other_question(driver)
        if len(driver.find_elements_by_class_name("choosable")) != 0:
            choose_question(driver, rough_answer_array, clicked_flag)
        else:
            blank_question(driver, rough_answer_array)

        time.sleep(1 + random.random()*2) 

def main():
    study_url   = "https://www.xuexi.cn/"

    driver = init_chromedriver(show_flag=True)
    driver.get(study_url)
    driver.implicitly_wait(5)

    # Home Page
    get_my_study_page(driver)

    # Exam
    get_exam_page(driver)

    # Practice
    try:
        driver.find_elements_by_class_name("block")[0].click()
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)
    except:
        print("[-]: Get Exam Practice Page Failed!")
        exit()
    
    # Do exam
    do_exam(driver)

    # Wait
    input("[+] Exam Done! Press Enter to finish.")

if __name__ == "__main__":
    main()