'''
 Chrome WebDriver Class
'''

import time
from selenium import webdriver
from bs4 import BeautifulSoup

class Driver:
    def __init__(self) -> None:
        self.options = webdriver.ChromeOptions()
        self.driver  = None
        self.html    = ""
        self.bs_form = ""

    def add_options(self, option) -> None:
        self.options.add_argument(option)
    
    def init_dirver(self, headless=True):
        if(headless):
            self.add_options('headless')
        
        self.add_options("disable-blink-features=AutomationControlled")
        
        self.driver  = webdriver.Chrome(options=self.options)

    def __get_bs_form(self):
        self.bs_form = BeautifulSoup(self.html, 'lxml')

    def get_html_source(self, url):
        self.driver.get(url)
        time.sleep(0.1)
        self.html = self.driver.page_source
        self.__get_bs_form()

    def save_html(self, html_file="test.html"):
        with open(html_file, 'w') as file_p:
            file_p.write(self.html)

    def find_all_by_class_name(self, class_name=""):
        find_results = []
        try:
            classes = self.bs_form.find_all(class_=class_name)

        except:
            print("[-] Warning: Find class '{}' failed!".format(class_name))

        for class_i in classes:
            find_results.append(class_i.get_text())

        return find_results

    
    def find_all_href_by_class_name(self, class_name="", base_url=""):
        find_results = {}
        try:
            classes = self.bs_form.find_all(class_=class_name)

        except:
            print("[-] Warning: Find class '{}' failed!".format(class_name))

        for class_i in classes:
            find_results.update({class_i.get_text() : base_url+class_i.get("href")})

        return find_results

    def find_all_by_meta_name(self, meta_name=""):
        find_results = []
        
        try:
            metas = self.bs_form.find_all(attrs={"name":meta_name})

        except:
            print("[-] Warning: Find '{}' meta name failed!".format(meta_name))

        for meta in metas:
            find_results.append(meta['content'])

        return find_results

    def find_all_by_meta_property(self, meta_property=""):
        find_results = []
        try:
            metas      = self.bs_form.find_all(attrs={"property":meta_property})

        except:
            print("[-] Warning: Find '{}' failed!".format(meta_property))

        for meta in metas:
            find_results.append(meta['content'])

        return find_results

    def find_by_class_name(self, class_name=""):
        find_result = ''
        try:
            find_result = self.bs_form.find(class_=class_name).get_text()

        except:
            print("[-] Warning: Find class '{}' failed!".format(class_name))


        return find_result

    def find_by_meta_name(self, meta_name=""):
        find_result = ''
        try:
            find_result = self.bs_form.find(attrs={"name":meta_name})['content']

        except:
            print("[-] Warning: Find '{}' meta name failed!".format(meta_name))

        return find_result

    def find_by_meta_property(self, meta_property=""):
        find_result = ''
        try:
            find_result  = self.bs_form.find(attrs={"property":meta_property})['content']

        except:
            print("[-] Warning: Get '{}' failed!".format(meta_property))

        return find_result

    def get_driver(self):
        return self.driver

    def driver_quit(self):
        self.driver.quit()

def main():
    url    = "http://irm.cninfo.com.cn/ircs/index"
    driver = Driver()
    driver.init_dirver()
    driver.get_html_source(url=url)
    
    html   = driver.html
    
    with open("test.html", 'w') as html_file:
        html_file.write(html)

    driver.driver_quit()

if __name__ == "__main__":
    main()