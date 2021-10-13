import os
import re
import time
import random
from taobao.item import Item

class Taobao:
    def __init__(self, driver) -> None:
        self.base_url    = "https://www.taobao.com/"
        self.login_url   = "https://login.taobao.com/member/login.jhtml"
        self.search_url  = 'https://s.taobao.com/search?q="{}"'
        self.driver      = driver
        self.total_pages = 1

    def login(self):
        self.driver.driver.get(self.base_url)
        print("[+] Please login ...")
        input("[+] After login, Enter to continue  ...")
        time.sleep(0.5 + random.random())

    def search(self, keyword, class_name="total"):
        search_url  = self.search_url.format(keyword)
        # search_url = 'file:///' + os.path.abspath('test.html')

        self.driver.get_html_source(search_url)

        # with open("test.html", 'w') as html_file:
        #     html_file.write(self.driver.html)

        try:
            total_string = self.driver.find_by_class_name(class_name=class_name)
            self.total_pages  = int(re.findall('\d+', total_string.strip())[0])
        except:
            self.total_pages  = 1

    def go_page(self, page_num=1):
        if page_num == 1 :
            return

    def goto_next_page(self):
        if self.driver.bs_form.find_all(class_="next-disabled"):
            print("[-] Warning: No Next page(s)!")
            return

        next_btn  = self.driver.driver.find_element_by_id("mainsrp-pager").find_element_by_class_name("next")

        try:
            self.driver.driver.execute_script("arguments[0].scrollIntoView();", next_btn)
            time.sleep(0.5 + random.random())
            next_btn.click()
        except:
            print("[-] Warning: Next page failed!")

        time.sleep(1 + random.random())
        self.driver.set_html_source()


    def get_items(self, class_name="J_MouserOnverReq"):

        items_arrays = []

        for page in range(self.total_pages):
            print("[+] Info: Getting {}/{}".format((page+1), self.total_pages), end='\r')

            try:
                items = self.driver.bs_form.find_all(class_=class_name)
            except:
                items = None
                print("[-] Warning: Find class '{}' failed!".format(class_name))

            for item_class in items:
                item_temp = Item()
                item_temp.price      = item_class.find(class_="price").get_text().strip()
                item_temp.sales      = item_class.find(class_="deal-cnt").get_text().strip()
                item_temp.location   = item_class.find(class_="location").get_text().strip()
                item_temp.shop       = item_class.find(class_="J_ShopInfo").get_text().strip()
                item_temp.shop_links = item_class.find(class_="J_ShopInfo").get("href")

                if not re.match(r'^http', item_temp.shop_links):
                    item_temp.links = 'https:' + item_temp.shop_links
                    
                try:
                    item_temp.name     = item_class.find_all(class_="J_ClickStat")[1].get_text().strip()
                    item_temp.links    = item_class.find_all(class_="J_ClickStat")[1].get("href")
                    if not re.match(r'^http', item_temp.links):
                        item_temp.links = 'https:' + item_temp.links
                except:
                    print("[-] Warning: Find name & links failed!".format(class_name))

                items_arrays.append(item_temp)

                # print("{}:\t{}:\t{}:\t{}:\t{}:\t{}:\t{}".format(item_temp.shop, item_temp.name, item_temp.price, item_temp.location, item_temp.sales, item_temp.links, item_temp.shop_links))
            
            if (page < (self.total_pages - 1)):
                self.goto_next_page()

        return items_arrays


    
