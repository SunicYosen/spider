"""
 Google Search
"""
import json
import urllib
from os import EX_CANTCREAT
from bs4 import BeautifulSoup

from webtools.driver import Driver
from excel import Excel

def main():
    base_url = "https://google.com/search?q={}&num={}"
    nums     = 50
    # desktop user-agent
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.72 Safari/537.36"
    # mobile user-agent
    MOBILE_USER_AGENT = "Mozilla/5.0 (Linux; Android 7.0; SM-G930V Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.125 Mobile Safari/537.36"
    
    proxies = { "http": "http://127.0.0.1:1081", "https": "http://127.0.0.1:1081", "socks5":"socks5://127.0.0.1:1081"}

    browser = Driver()
    browser.init_dirver()

    excel = Excel(file_name="result.xlsx")
    
    keywords = ["self-clarity scale", "self-clarification scale", "self-esteem scale", "自尊量表", "自我概念清晰度量表"]

    results = {}

    for keyword in keywords:
        print("[+]: searching {}".format(keyword))
        keyword = keyword.replace(' ', '+')
        url     = base_url.format(keyword, nums)
        browser.get_html_source(url=url)

        soup = BeautifulSoup(browser.html, "html.parser")

        keyword_result = []

        for g in soup.find_all('div', class_='g'):
            anchors = g.find_all('a')
            if anchors:
                link = anchors[0]['href']
                title = g.find('h3').text
                item = {
                    "title": title,
                    "link": link
                }
                keyword_result.append(item)

            excel.write(sheet_name=keyword, data_array=[title, link])

        results.update({keyword: keyword_result})

        json.dumps(results)

if __name__ == "__main__":
    main()
