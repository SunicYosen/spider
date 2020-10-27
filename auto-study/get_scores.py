
'''
 Get Score
'''
import time

def get_scores(driver, url):

    # 获取当前积分
    driver.get(url)
    time.sleep(2)

    gross_score = 0
    today_score = 0
    titles = []
    scores = []

    try:
        gross_score = driver.find_element_by_xpath("//*[@id='app']/div/div[2]/div/div[2]/div[2]/span[1]").get_attribute('innerText')
        today_score = driver.find_element_by_xpath("//span[@class='my-points-points']").get_attribute('innerText')

        titles = driver.find_elements_by_class_name("my-points-card-title")
        scores = driver.find_elements_by_class_name("my-points-card-text")
    except:
        print("[-]: Get Scores Failed! Cannot find score items in page.")

    if (len(titles) != len(scores)) or (len(titles) == 0):
        print("[-]: Get Scores Error!")

    time.sleep(2)

    scores_list   = []
    scores_titles = []
    scores_list.append(gross_score)
    scores_titles.append("成长总积分")
    scores_list.append(today_score)
    scores_titles.append("今日累积积分")

    print("[+]: - 成长总积分: " + str(gross_score))
    print("[+]: - 今日累积积分: " + str(today_score))

    for index, score_title in enumerate(titles):
        scores_list.append(scores[index].get_attribute('innerText'))
        scores_titles.append(score_title.get_attribute('innerText'))
        print("[+]: -- " + score_title.get_attribute('innerText') + "\t:" + scores[index].get_attribute('innerText'))

    return scores_list, scores_titles

