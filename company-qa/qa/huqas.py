"""
Shen Zhen QA
"""

import time
from datetime import datetime

from qa import QA
from webtools.driver import Driver

class HuQAS():
    def __init__(self, url) -> None:
        self.qas    = []
        self.driver = Driver()
        self.driver.init_dirver(headless=False)
        self.base_url = url

    def go_to_base_page(self):
        self.driver.driver.get(self.base_url)
        time.sleep(0.5)

    def set_keyword(self, search_id="top_search_txt", keyword="", button_id="top_search"):
        self.driver.driver.find_element_by_id(search_id).send_keys(keyword)
        time.sleep(0.5)
        self.driver.driver.find_element_by_id(button_id).click()
        time.sleep(0.5)
        
    def click_change_page(self, click_class=""):
        pass

    def scroll_bottom(self, class_name="next"):
        next_btn = self.driver.driver.find_element_by_class_name(class_name)
        self.driver.driver.execute_script("arguments[0].scrollIntoView();", next_btn)
        time.sleep(0.5)

    def get_qas(self, class_name="m_feed_item"):
        questions = self.driver.driver.find_elements_by_class_name(class_name)

        for question in questions:
            q_a = QA()

            try:
                question_q       = question.find_elements_by_class_name("m_feed_txt")[0].text
                q_a.company_name = (question_q.split(')')[0]).split('(')[0].strip().replace(':', '')
                q_a.company_code = (question_q.split(')')[0]).split('(')[1].strip()
                q_a.question     = (question_q.split(')')[1]).strip()
            except:
                q_a.company_name = "NONE"
                q_a.company_code = "NONE"
                q_a.question     = "NONE"

            try:
                q_a.q_time       = question.find_elements_by_class_name("m_feed_from")[0].text
            except:
                q_a.q_time       = "NONE"

            try:
                q_a.answer = question.find_elements_by_class_name("m_feed_txt")[1].text
                q_a.a_time = question.find_elements_by_class_name("m_feed_from")[1].text
            except:
                q_a.answer = "NONE"
                q_a.a_time = "NONE"

            self.qas.append(q_a)
            # print(q_a.a_time)
    
    def click_next_page(self, class_name="next"):
        next_btn = self.driver.driver.find_element_by_class_name(class_name)
        self.driver.driver.execute_script("arguments[0].scrollIntoView();", next_btn)
        time.sleep(0.5)
        next_btn.click()
        time.sleep(1)

def main():
    base_url  = "http://sns.sseinfo.com/"
    lmt_date  = datetime.strptime("2020-09-01",  "%Y-%m-%d")
    key_words = ["华为"]

    huqa = HuQAS(base_url)

    for keyword in key_words:
        huqa.go_to_base_page()
        huqa.set_keyword(keyword=keyword)
        huqa.click_change_page()
        while(True):
            huqa.scroll_bottom()
            huqa.get_qas()

            try:
                last_time = datetime.strptime(huqa.qas[-1].q_time, "%Y-%m-%d")
            except:
                last_time = lmt_date

            if (last_time < lmt_date):
                break

            huqa.click_next_page()

if __name__ == "__main__":
    main()

