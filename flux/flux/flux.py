
import os
import re
import time
import json
import random

class Flux:
    def __init__(self, driver) -> None:
        self.base_url         = "http://www.5lux.com/"
        self.brands_cat_url   = "http://www.5lux.com/brand"
        self.driver           = driver
        self.done_brands      = {}

        self.brands_dict = {}
    
    def get_brand_list(self, url):
        if os.path.exists(url):
            self.driver.get_html_source_from_file(url)
        else:
            self.driver.get_html_source(url)

        brands_cat = self.driver.find_all_by_id("letter_a")

        for brand_cat in brands_cat:
            brands_dict = {}
            cat_name    = brand_cat.find("dt").get_text()
            brands_li   = brand_cat.find_all("li")
            
            for brand_li in brands_li:
                brand_name = brand_li.a.get("title")
                brand_link = brand_li.a.get("href")
                self.brands_dict.update({brand_name:{'link': brand_link}})

    def dump_brands(self, json_file):
        with open(json_file, 'w', encoding="utf-8") as f:
            json.dump(self.brands_dict, f, ensure_ascii=False,indent = 4)
            f.close()

    def dump_done_brands(self, json_file):
        with open(json_file, 'w', encoding="utf-8") as f:
            json.dump(self.done_brands, f, ensure_ascii=False,indent = 4)
            f.close()

    def load_brands(self, json_file):
        if os.path.exists(json_file):
            with open(json_file, 'r') as json_fp:
                json_data         = json_fp.read()
                self.brands_dict  = json.loads(json_data)
                json_fp.close()
        else:
            self.get_brand_list(self.brands_cat_url)

    def load_done_brands(self, json_file):
        if os.path.exists(json_file):
            with open(json_file, 'r') as json_fp:
                json_data         = json_fp.read()
                self.done_brands  = json.loads(json_data)
                json_fp.close()
        else:
            self.done_brands      = {}
            
    def get_pages(self):
        pages = []
        pages_classes = []

        try:
            pages_classes = self.driver.find_by_class_name("pages_des").find_all('a', class_="pages_nums")
        except:
            pass

        for page_a in pages_classes:
            pages.append(page_a.get("href"))

        return pages

    def get_items_list(self):
        items_array = []
        items_li = self.driver.find_by_class_name("stblock_body").find_all("dd")

        for item_li in items_li:
            item_link = item_li.find('a').get('href')
            items_array.append(item_link)

        return items_array


    def get_brand_items(self, url):
        items_array = []

        if os.path.exists(url):
            self.driver.get_html_source_from_file(url)
        else:
            self.driver.get_html_source(url)

        brand_name = self.driver.find_by_class_name("dbir_head").dl.dd.get_text()
        items_array += self.get_items_list()

        pages_array = self.get_pages()

        for page_link in pages_array:
            self.driver.get_html_source(page_link)
            items_array += self.get_items_list()

        return items_array

    def get_item_info(self, url):
        item_info = {}

        if os.path.exists(url):
            self.driver.get_html_source_from_file(url)
        else:
            self.driver.get_html_source(url)

        name = "-"
        price = "-"
        favorite = "-"

        try:
            name  = self.driver.find_by_class_name("clearfixgd").dl.find_all('dd')[1].a.get_text()
        except:
            print("[-] Get name failed from: {}".format(url))

        try:
            price = self.driver.find_by_class_name("fsk_goods_price").get_text().replace('\n', '').replace(' ', '').strip()
        except:
            print("[-] Get price failed from: {}".format(url))

        try:
            favorite = re.findall(r"\d+", self.driver.find_by_class_name("add_collect_bt").p.get_text())[0]
        except:
            print("[-] Get favorite failed from: {}".format(url))
        

        item_info = {'name': name, 'price': price, 'favorite': favorite, 'url':url}

        # print(item_info)

        return item_info

    def get_all(self, json_file, json_done_file):
        i = 0
        for key in self.brands_dict.keys():
            i += 1

            if key not in self.done_brands.keys():
                print("[+]: Processing {}/{} {} ...".format(i,len(self.brands_dict), key))
                items_info_array = []
                items_list_link  = self.brands_dict[key]['link']
                items_link_array = self.get_brand_items(items_list_link)
                j = 0
                for item_link in items_link_array:
                    j += 1
                    print("     ...... {}/{}".format(j,len(items_link_array)), end='\r')
                    item_info_dict = self.get_item_info(item_link)
                    items_info_array.append(item_info_dict)

                self.brands_dict[key].update({'items':items_info_array})
                self.done_brands.update({key: len(items_info_array)})

                self.dump_brands(json_file)
                self.dump_done_brands(json_done_file)

    def write_excel(self, excel, excel_title, sheet_name = "5LUX"):
        excel.write(sheet_name, excel_title)
        for brand in self.brands_dict.keys():
            brand_data = []
            for item in self.brands_dict[brand]["items"]:
                item_info = [brand]
                for title in excel_title[1:]:
                    item_info.append(item[title])

                brand_data.append(item_info)

            excel.write_list(sheet_name, brand_data)
