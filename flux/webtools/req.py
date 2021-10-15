'''
 Chrome WebDriver Class
'''
import os
import time
import random
import requests
from requests.models import Response
from bs4 import BeautifulSoup

class Req:
    def __init__(self) -> None:
        self.html    = ""
        self.bs_form = ""

    def __get_bs_form(self):
        self.bs_form = BeautifulSoup(self.html, 'lxml')

    def get_html_source(self, url):
        time.sleep(0.1 + (random.random()/10))
        requests_session  = requests.session()
        response          = requests_session.get(url)
        response.encoding = response.apparent_encoding
        self.html         = response.text
        self.__get_bs_form()
        # self.html       = lxml.etree.HTML(data)

    def get_html_source_from_file(self, file_path):

        with open(file_path, 'r', encoding='utf-8') as fp:
            self.html         = fp.read()

        self.__get_bs_form()
        
        # self.html       = lxml.etree.HTML(data)

    # def set_html_source(self):
    #     self.html = self.driver.page_source
    #     self.__get_bs_form()

    def save_html(self, html_file="test.html"):
        with open(html_file, 'w') as file_p:
            file_p.write(self.html)

    def find_all_text_by_class_name(self, class_name=""):
        find_results = []
        try:
            classes = self.bs_form.find_all(class_=class_name)

        except:
            print("[-] Warning: Find class '{}' failed!".format(class_name))

        for class_i in classes:
            find_results.append(class_i.get_text())

        return find_results

    def find_all_by_class_name(self, class_name=""):
        classes = []
        try:
            classes = self.bs_form.find_all(class_=class_name)

        except:
            print("[-] Warning: Find class '{}' failed!".format(class_name))


        return classes

    def find_all_by_id(self, id=""):
        items = []
        try:
            items = self.bs_form.find_all(id=id)

        except:
            print("[-] Warning: Find class '{}' failed!".format(id))


        return items

    
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

    def find_text_by_class_name(self, class_name=""):
        find_result = ''
        try:
            find_result = self.bs_form.find(class_=class_name).get_text()

        except:
            print("[-] Warning: Find class '{}' failed!".format(class_name))


        return find_result

    def find_by_class_name(self, class_name=""):
        class_item = None
        try:
            class_item = self.bs_form.find(class_=class_name)

        except:
            print("[-] Warning: Find class '{}' failed!".format(class_name))


        return class_item

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
    url    = "http://www.5lux.com/brand"
    req    = Req()
    req.get_html_source(url=url)
    req.save_html("../htmls/list.html")


if __name__ == "__main__":
    main()