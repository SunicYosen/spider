"""
Shen Zhen QA
"""

import time
from datetime import datetime

from qa import QA
from webtools.driver import Driver

class ShenQA():
    def __init__(self, url) -> None:
        self.qas    = []
        self.driver = Driver()
        self.driver.init_dirver(headless=False)
        self.base_url = url

    def go_to_base_page(self):
        self.driver.driver.get(self.base_url)
        time.sleep(1)

    def set_keyword(self, search_id="header-search", keyword="", button_class="el-input__suffix-inner"):
        self.driver.driver.find_element_by_id(search_id).send_keys(keyword)
        time.sleep(0.5)
        self.driver.driver.find_element_by_class_name(button_class).click()
        time.sleep(0.5)
        
    def click_change_page(self, click_id="tab-2"):
        self.driver.driver.find_element_by_id(click_id).click()
        time.sleep(1)

    def get_qas(self, class_name="item-question"):
        questions = self.driver.driver.find_elements_by_class_name(class_name)

        for question in questions:
            q_a = QA()

            try:
                q_a.company_name = question.find_element_by_class_name("companyName").text
            except:
                q_a.company_name = "NONE"

            try:
                q_a.company_code = question.find_element_by_class_name("company-code").text
            except:
                q_a.company_code = "NONE"

            try:
                q_a.qa_time      = question.find_element_by_class_name("question-time").text
            except:
                q_a.qa_time      = "NONE"
            
            try:
                q_a.question     = question.find_element_by_class_name("question-content").text
            except:
                q_a.question     = "NONE"
            
            try:
                q_a.answer       = question.find_element_by_class_name("reply-content").text
            except:
                q_a.answer       = "NONE"

            self.qas.append(q_a)
            # print(q_a.question)
    
    def click_next_page(self, class_name="btn-next"):
        next_btn = self.driver.driver.find_element_by_class_name(class_name)
        self.driver.driver.execute_script("arguments[0].scrollIntoView();", next_btn)
        time.sleep(0.5)
        next_btn.click()
        time.sleep(0.5)

def main():
    base_url  = "http://irm.cninfo.com.cn/"
    lmt_date  = datetime.strptime("2020-09-01",  "%Y-%m-%d")
    key_words = ["华为"]

    shenqa = ShenQA(base_url)

    for keyword in key_words:
        shenqa.go_to_base_page()
        shenqa.set_keyword(keyword=keyword)
        shenqa.click_change_page()
        while(True):
            shenqa.get_qas()
            try:
                last_time = datetime.strptime(shenqa.qas[-1].qa_time, "%Y-%m-%d")
            except:
                last_time = lmt_date

            if (last_time < lmt_date):
                break

            shenqa.click_next_page()

if __name__ == "__main__":
    main()

