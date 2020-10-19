'''
 Read Article
'''
import time
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from get_usr_data_dir import get_usr_data_dir

# 阅读文章
def read_articles(driver, urls=[]):
    for num, url in enumerate(urls):
        print("[+]: Reading: ", num+1, '/',len(urls))
        driver.get(url)
        driver.implicitly_wait(10)
        articles = driver.find_elements_by_xpath("//div[@class='text-link-item-title']")

        for index, article in enumerate(articles):
            if index > 4:
                break

            article.click()
            all_handles = driver.window_handles
            driver.switch_to.window(all_handles[-1])
            driver.get(driver.current_url)
            print("[+]: --", index+1, '/', 5, '\t', driver.current_url)
            # driver.save_screenshot('article'+str(num)+'_'+str(index)+'.png')
            
            # Scroll down
            for i in range(0, 2000, 100):
                js_code = "var q=document.documentElement.scrollTop=" + str(i)
                driver.execute_script(js_code)
                time.sleep(2)

            # Scroll up
            for i in range(2000, 0, -100):
                js_code = "var q=document.documentElement.scrollTop=" + str(i)
                driver.execute_script(js_code)
                time.sleep(2)

            time.sleep(2)
            driver.close()

            # Return Home page
            driver.switch_to.window(all_handles[0])

    print("[+]: 阅读文章完毕\n")

def main():
    option = webdriver.ChromeOptions()
    option.add_argument('disable-infobars')
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    user_data_path = get_usr_data_dir()
    chrome_options.add_argument(user_data_path)

    driver = webdriver.Chrome(options=chrome_options)

    driver.get("https://www.xuexi.cn/")
    driver.implicitly_wait(5)
    article_urls = ["https://www.xuexi.cn/xxqg.html?id=36a1bf1b683942fe917fc1866f13fc21","https://www.xuexi.cn/xxqg.html?id=2813415f8e1c48b4b47e794aca7b7bb5"]
    videos_url   = 'https://www.xuexi.cn/4426aa87b0b64ac671c96379a3a8bd26/db086044562a57b441c24f2af1c8e101.html'
    score_url    = 'https://pc.xuexi.cn/points/my-points.html'
    read_articles(driver, article_urls)     # 阅读文章

    # watch_videos(videos_url)      # 观看视频
    # get_scores(score_url)         # 获得今日积分

    driver.quit()

if __name__ == '__main__':
    main()