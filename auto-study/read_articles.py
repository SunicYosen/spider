'''
 Read Article
'''
import os
import time
import csv
import re
import random
import datetime
from init_chromedriver import init_chromedriver

def get_article_urls(csv_filename):

    article_urls = {}

    if not os.path.exists(csv_filename):
        print("[-]: Read Articles Failed! CSV file doesn't exist!")
        return article_urls

    csv_file     = open(csv_filename, "r", encoding='utf-8')
    csv_lines    = csv.reader(csv_file)

    for article_url in csv_lines:
        article_urls[article_url[0]] = article_url[1]

    csv_file.close()

    return article_urls

# 阅读文章
def read_articles(driver, csv_filename="articles.csv", read_mode=1):
    article_urls = get_article_urls(csv_filename)

    if not article_urls:
        print("[-]: Read Articles Failed! CSV file is blank.")
        return

    for num, articles_list_name in enumerate(article_urls):
        articles_list_url  = article_urls[articles_list_name]
        print("[+]: Reading: ", num + 1, '/',len(article_urls), articles_list_name)

        if read_mode == 0:
            random.seed(datetime.datetime.now())
            read_num = random.randint(0, 2)
        else:
            read_num = read_mode

        driver.get(articles_list_url)
        driver.implicitly_wait(3 + random.randint(0, 2))

        articles = driver.find_elements_by_xpath("//div[@class='text-link-item-title']")
        for index, article in enumerate(articles):
            if index > read_num-1:
                break

            article.click()
            all_handles = driver.window_handles
            driver.switch_to.window(all_handles[-1])
            driver.get(driver.current_url)
            print("[+]: --", index + 1, '/', read_num, '\t', driver.current_url)
            
            # Scroll down
            for i in range(0, 2000, 100):
                js_code = "var q=document.documentElement.scrollTop=" + str(i)
                driver.execute_script(js_code)
                time.sleep(1.5 + random.random())

            # Scroll up
            for i in range(2000, 0, -200):
                js_code = "var q=document.documentElement.scrollTop=" + str(i)
                driver.execute_script(js_code)
                time.sleep(1 + random.random())

            time.sleep(1 + random.random())
            driver.close()

            # Return Home page
            driver.switch_to.window(all_handles[0])

    print("[+]: 阅读文章完毕\n")

def main():
    driver = init_chromedriver(show_flag=True)
    read_articles(driver, csv_filename="articles.csv", read_mode=1)  # 阅读文章
    driver.quit()

if __name__ == '__main__':
    main()