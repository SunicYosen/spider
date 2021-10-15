"""
 Taobao Search
"""
import json
import urllib
from os import EX_CANTCREAT
from bs4 import BeautifulSoup

from flux.flux import Flux 
from webtools.req import Req
from excel import Excel

def main():
    result_excel = "data/result.xlsx"
    brands_json  = "data/brands.json"
    brands_done  = "data/brands_done.json"
    excel_title  = ["shop", "name", "price", "favorite", "url"]

    browser = Req()
    flux    = Flux(browser)
    excel   = Excel(file_name=result_excel)

    flux.load_brands(brands_json)
    flux.load_done_brands(brands_done)
    flux.get_all(brands_json, brands_done)
    flux.write_excel(excel, excel_title)

if __name__ == "__main__":
    main()
