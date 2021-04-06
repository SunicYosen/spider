
import time

from do_exam import do_exam

def get_weekly_list_page(driver):
    try:
        driver.find_elements_by_class_name("block")[1].click()
        driver.switch_to.window(driver.window_handles[-1])
        time.sleep(1)

    except:
        print("[-]: Get Exam Weekly List Page Failed!")
        exit()

def get_weekly_last(driver):
    weekly_got  = False

    while not weekly_got:
        weekly_list = driver.find_elements_by_tag_name("button")

        for week in weekly_list:
            if week.get_attribute("innerText") == "开始答题":
                driver.execute_script("arguments[0].scrollIntoView();", week)
                time.sleep(0.5)
                week.click()
                weekly_got = True
                time.sleep(0.5)
                break

        if not weekly_got:
            next_page_button = driver.find_element_by_class_name(' ant-pagination-next')
            if next_page_button:
                driver.execute_script("arguments[0].scrollIntoView();", next_page_button)
                next_page_button.click()
                time.sleep(0.5)
            else:
                print("[-]: 没有找到可用的本周答题！")

def weekly_exam(driver, url='https://pc.xuexi.cn/points/exam-index.html', questions_per_week=5):
    print("[+]: Do Weekly Exam - ", questions_per_week, "Question(s) per Week.")
    try:
        driver.get(url)
    except:
        print("[-]: Weekly Exam Failed! Get Exam Page Error!")
        return
    
    time.sleep(1)
    
    get_weekly_list_page(driver)
    get_weekly_last(driver)
    do_exam(driver)
    print("[+]: 完成每周答题！")