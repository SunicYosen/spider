"""
 Taobao Search
"""
import json
import urllib
from os import EX_CANTCREAT
from bs4 import BeautifulSoup

from taobao.taobao import Taobao 
from webtools.driver import Driver
from excel import Excel

def main():
    browser = Driver()
    browser.init_dirver(headless=False)
    excel   = Excel(file_name="result.xlsx")
    tb      = Taobao(browser)

    keywords = ["Pico G2 4KS"]
    excel_title = ["名称", "价格", "月销量", "店铺", "地址", "商品链接", "店铺链接"]

    results = {}

    for keyword in keywords:
        print("[+]: searching {} ...".format(keyword))
        keyword = keyword.replace(' ', '+')

        

        excel.write(sheet_name=keyword, data_array=excel_title)

        tb.login()
        tb.search(keyword)
        results = tb.get_items()

        for item in results:
            item_data = [item.name, item.price, item.sales, item.shop, item.location, item.links, item.shop_links]
            excel.write(sheet_name=keyword, data_array=item_data)

if __name__ == "__main__":
    main()
