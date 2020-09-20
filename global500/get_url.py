'''
Func: Get data of global-500
'''

from lxml import etree
import requests
import time

def get_url_global500(root_url, numbers, pre_url='https://www.caifuzhongwen.com/fortune500/'):
    link_array     = []

    try:
        data       = requests.get(root_url).text
        s          = etree.HTML(data)
        rank_table = s.xpath("/html/body/main/div[1]/div[10]/div[2]/table/tbody")[0]

        for i in range(500):
            company_rank    = rank_table.xpath('./tr[{}]/td[1]/i/text()'.format(i+2))[0]
            company_link    = rank_table.xpath('./tr[{}]/td[2]/a/@href'.format(i+2))[0]
            company_name    = rank_table.xpath('./tr[{}]/td[2]/a/text()'.format(i+2))[0].encode('iso-8859-1').decode('utf-8')
            company_name_en = rank_table.xpath('./tr[{}]/td[2]/a/text()[2]'.format(i+2))[0].encode('iso-8859-1').decode('utf-8')
            full_link       = pre_url+company_link.replace('../','')
            link_array.append(full_link)

    except:
        print("ERROR: Error parse the website content!\n")
    
    print("[+] Info: Got all urls!")
    return link_array


if __name__ == '__main__':
    get_url_global500("https://www.caifuzhongwen.com/fortune500/paiming/global500/2020_%E4%B8%96%E7%95%8C500%E5%BC%BA.htm", 500)
