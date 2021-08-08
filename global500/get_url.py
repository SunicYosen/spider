'''
Func: Get data of global-500
'''

from os import link
from requests.models import Response
from lxml import etree
import requests
import time

def get_url_global500(root_url, numbers=500, pre_url='https://www.caifuzhongwen.com/fortune500/', tags_number=10):
    link_array     = []
    name_array     = []

    try:

        requests_session = requests.session()
        
        response = requests_session.get(root_url)
        response.encoding = response.apparent_encoding
        data=response.text
        request_html          = etree.HTML(data)

        # 2021
        # rank_table = request_html.xpath("/html/body/main/div[1]/div[12]/div[2]/table/tbody")[0]
        # 2020
        rank_table = request_html.xpath("/html/body/main/div[1]/div[{}]/div[2]/table/tbody".format(tags_number))[0]

        for i in range(numbers):
            company_rank    = rank_table.xpath('./tr[{}]/td[1]/i/text()'.format(i+2))[0]
            company_link    = rank_table.xpath('./tr[{}]/td[2]/a/@href'.format(i+2))[0]
            company_name    = rank_table.xpath('./tr[{}]/td[2]/a/text()'.format(i+2))[0]
            company_name_en = rank_table.xpath('./tr[{}]/td[2]/a/text()[2]'.format(i+2))[0]
            full_link       = pre_url+company_link.replace('../','')
            link_array.append(full_link)
            name_array.append(company_name)

    except:
        print("ERROR: Error parse the website content!\n")
    
    print("[+] Info: Got all urls!")
    return link_array, name_array


if __name__ == '__main__':
    link_array, name_array = get_url_global500("https://www.caifuzhongwen.com/fortune500/paiming/global500/2021_%e4%b8%96%e7%95%8c500%e5%bc%ba.htm", 500, tags_number=12)
    # print(link_array)
