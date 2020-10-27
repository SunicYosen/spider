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
                time.sleep(1 + random.random())

    # The First Default
    if (clicked_flag == False):
        choosable_array[0].click()
    time.sleep(1 + random.random())

    try:
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
        driver.find_elements_by_tag_name("button")[0].click()
    except:
        print("[-]: Click Next Question Failed!")
        return

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
    try:
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("question")[0])
        blankArr = driver.find_elements_by_class_name("blank")
    except:
        print("[-]: Find Blak Failed!")
        return

    for i in range(len(blankArr)):
        blankArr[i].send_keys(rough_answer_array[i])
        time.sleep(0.5 + random.random())

    time.sleep(1 + random.random()*2)

    try:
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
        driver.find_elements_by_tag_name("button")[0].click()
    except:
        print("[-]: Click Next Question Failed!")
        return

    time.sleep(1 + random.random()*2)

    for i in driver.find_elements_by_tag_name("button"):
        if (i.get_attribute("innerText") == "下一题"):
            i.click()

        # For Special exam
        elif (i.get_attribute("innerText") == "交 卷"):
            print("[+]: 交卷")
            i.click()
    
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
    try:
        driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
        driver.find_elements_by_tag_name("button")[0].click()
    except:
        print("[-]: Click Next Question Failed!")
        return
    
    time.sleep(1 + random.random()*2)

    for i in driver.find_elements_by_tag_name("button"):
        if (i.get_attribute("innerText") == "下一题"):
            i.click()

        # For Special exam
        elif (i.get_attribute("innerText") == "交 卷"):
            print("[+]: 交卷")
            i.click()
    
    time.sleep(1 + random.random()*2)

def video_question(driver):
    if (len(driver.find_elements_by_class_name("choosable")) != 0):
        try:
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("choosable")[0])
            driver.find_elements_by_class_name("choosable")[0].click()
        except:
            print("[-]: Video Question Error! Scroll into answer viewer failed.")
            return
        
        try:
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
            driver.find_elements_by_tag_name("button")[0].click()
            time.sleep(1 + random.random())
        except:
            print("[-]: Video Question Error! Click Sure Button failed")
            return
        # try:
        #     driver.find_elements_by_tag_name("button")[0].click()
        #     time.sleep(1 + random.random()*2)
        # except:
        #     print("[-]: Video Question Error! Click Next Button failed.")
        #     return
    else:
        try:
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("blank")[0])
            videoBlankArr = driver.find_elements_by_class_name("blank")
            for blank in videoBlankArr:
                blank.send_keys("不知道")
        except:
            print("[-]: Video Question Error. Filling Blank Failed!")
        try:
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_tag_name("button")[0])
            driver.find_elements_by_tag_name("button")[0].click()
            time.sleep(1 + random.random())
        except:
            print("[-]: Video Question Error! Click Sure Button failed")
            return

        # try:
        #     driver.find_elements_by_tag_name("button")[0].click()
        #     time.sleep(1 + random.random()*2)
        # except:
        #     print("[-]: Video Question Error! Click Next Button failed")
        #     return

    for i in driver.find_elements_by_tag_name("button"):
        if (i.get_attribute("innerText") == "下一题"):
            i.click()

        # For Special exam
        elif (i.get_attribute("innerText") == "交 卷"):
            print("[+]: 交卷")
            i.click()
    
    time.sleep(1 + random.random()*2)

def get_rough_answer(driver, rough_answer_array):
    try:
        fontArr = driver.find_elements_by_tag_name("font")
        for fontEL in fontArr:
            if (fontEL.get_attribute("innerText") != ""):
                rough_answer_array.append(fontEL.get_attribute("innerText"))
    except:
        print("[-]: Cannot find answer in tips.")
        return

def get_pager_now(driver):
    try:
        pager_now = driver.find_elements_by_class_name("big")[0].get_attribute("innerText")
        return int(pager_now)
    except:
        print("[-]: Get Current Pager Error! Return 0.")
        return -1

def get_pager_all(driver):
    try:
        pager_all_str = driver.find_elements_by_class_name("pager")[0].get_attribute("innerText")
        pager_all     = pager_all_str.split("/")[1]
        return int(pager_all)
    except:
        print("[-]: Get All Pager Num Error! Return 0.")
        return -1

# Do exam
def do_exam(driver, questions_per_group=5):
    current_page       = 0
    all_page           = questions_per_group
    clicked_flag       = False
    rough_answer_array = []
    random.seed(datetime.datetime.now())

    print("[+]: Doing Exam.")

    while(current_page < all_page):
        # Get Current pager
        current_page_temp       = get_pager_now(driver)
        all_page_temp           = get_pager_all(driver)
        if current_page_temp == -1:
            current_page += 1
        else:
            current_page =  current_page_temp
        
        if all_page_temp == -1:
            all_page = questions_per_group
        else:
            all_page = all_page_temp

        time.sleep(1 + random.random()*2)
        rough_answer_array.clear()

        print("[+]: -- ", current_page, '/', all_page)

        # If next practice
        next_practice(driver)

        if(len(driver.find_elements_by_class_name("tips")) != 0):
            try:
                driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("tips")[0])
                driver.find_elements_by_class_name("tips")[0].click()
            except:
                print("[-] Try to open tips Error! Trying again ... ")
                break

            if (driver.find_elements_by_class_name("line-feed")[0].get_attribute("innerText") == "请观看视频"):
                try:
                    driver.find_elements_by_class_name("tips")[0].click()
                    video_question(driver)
                except:
                    print("[-] Video Question Error!")
                    break

            # Get Rough Answer from tips
            get_rough_answer(driver, rough_answer_array)
            time.sleep(1 + random.random()*2)

            try:
                # Close tips
                driver.find_elements_by_class_name("tips")[0].click()
            except:
                print("[-]: Close tips Error! Trying again ...")
                break

            time.sleep(1 + random.random()*2)
            # print(rough_answer_array)

        try:
            # Scroll to question
            driver.execute_script("arguments[0].scrollIntoView();", driver.find_elements_by_class_name("question")[0])
            time.sleep(1 + random.random()*2)
        except:
            print("[-]: Scroll to question failed. Trying again ...")
            break

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
    input("[+]: Exam Done! Press Enter to finish.")

if __name__ == "__main__":
    main()