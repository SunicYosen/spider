'''
Func: Get data of global-500
'''
import os
import json
from lxml import etree
import requests
import time
from get_url import get_url_global500

from company import Company

def get_data_load_file(data_json="data.json"):
    company_list = []
    company_json_list = []

    if os.path.isfile(data_json):
        try:
            with open(data_json, 'r', encoding="utf-8") as f:
                company_json_list = json.load(f)
        except:
            print("[-]: Load cat json failed!")
            os.remove(data_json)

    for company in company_json_list:
        company_class = Company()
        company_class.set_data(company)
        company_list.append(company_class)

    return company_list


def get_data_global500(root_url, data_json="data.json", url_tag=10):
    numbers           = 500
    index             = 0
    company_list      = []
    company_json_list = []
    company_urls,name = get_url_global500(root_url, numbers, tags_number=url_tag)
    time_begin        = time.time()

    got_data = False

    if os.path.isfile(data_json):
        try:
            with open(data_json, 'r', encoding="utf-8") as f:
                company_list = get_data_load_file(data_json)
            got_data = True
        except:
            print("[-]: Load cat json failed!")
            os.remove(data_json)
            got_data = False

    if not company_list:
        got_data = False
    
    if not got_data:
        for company_url in company_urls:
            index     = index + 1
            duration  = round(time.time() - time_begin, 2)
            remaining = round(duration * numbers / (index) - duration, 2)
            print("[+] Getting Data :{}/{}，Cost Time: {}s， Remainimg: {}s".format(index, numbers, duration, remaining), end="\r")
            
            try:
                url = company_url
                data = requests.get(url).text
                time.sleep(0.01)
                s=etree.HTML(data)

                company         = s.xpath("/html/body/main/div[1]/div[4]/div/h1/text()")[0].encode('iso-8859-1').decode('utf-8')
                company_en      = s.xpath("/html/body/main/div[1]/div[4]/div/h1/small/text()")[0].encode('iso-8859-1').decode('utf-8')
                carousel_slide0 = s.xpath('//*[@id="carousel-slide"]/div/div[1]/div')[0]
                carousel_slide1 = s.xpath('//*[@id="carousel-slide"]/div/div[2]/div[2]')[0]

                revenue  = carousel_slide0.xpath("./div[1]/div[1]/ul/li[1]/p/text()[2]")[0].replace(',','')
                profit   = carousel_slide0.xpath("./div[1]/div[1]/ul/li[3]/p/text()[2]")[0].replace(',','')
                rank     = carousel_slide0.xpath("./div[1]/div[2]/p[2]/b/text()")[0]
                ceo      = carousel_slide0.xpath("./div[2]/table/tr[1]/td[2]/text()")[0]
                country  = carousel_slide0.xpath("./div[2]/table/tr[2]/td[2]/text()")[0].encode('iso-8859-1').decode('utf-8')
                industry = carousel_slide0.xpath("./div[2]/table/tr[3]/td[2]/text()")[0].encode('iso-8859-1').decode('utf-8')
                city     = carousel_slide0.xpath("./div[2]/table/tr[4]/td[2]/text()")[0].encode('iso-8859-1').decode('utf-8')
                employee = carousel_slide0.xpath("./div[2]/table/tr[5]/td[2]/text()")[0]
                website  = carousel_slide0.xpath("./div[2]/table/tr[6]/td[2]/text()")[0]

                revenue_change_percent = carousel_slide1.xpath("./table/tr[2]/td[3]/text()")[0]
                profit_change_percent  = carousel_slide1.xpath("./table/tr[3]/td[3]/text()")[0]
                total_money            = carousel_slide1.xpath("./table/tr[4]/td[2]/text()")[0].replace(',','')
                shareholders_equity    = carousel_slide1.xpath("./table/tr[5]/td[2]/text()")[0].replace(',','')

                company_temp = Company()
                company_temp.company_name           = company
                company_temp.company_name_en        = company_en
                company_temp.rank                   = rank
                company_temp.industry               = industry
                company_temp.revenue                = revenue
                company_temp.country                = country
                company_temp.city                   = city
                company_temp.employee               = employee
                company_temp.revenue_change_percent = revenue_change_percent
                company_temp.profit                 = profit
                company_temp.profit_change_percent  = profit_change_percent
                company_temp.total_money            = total_money
                company_temp.shareholders_equity    = shareholders_equity
                company_temp.ceo                    = ceo
                company_temp.website                = website
                company_temp.data_site              = company_url
                company_list.append(company_temp)
                company_json_list.append(dict(company_temp))

            except:
                print("ERROR: Error parse the website content!\n")
        
        with open(data_json, 'w', encoding="utf-8") as f:
                json.dump(company_json_list, f, ensure_ascii=False, indent = 4)

    print("\n[+] Info: Got All Data! ")
    return company_list

if __name__ == '__main__':
   company2021_list = get_data_global500("https://www.caifuzhongwen.com/fortune500/paiming/global500/2021_%e4%b8%96%e7%95%8c500%e5%bc%ba.htm", data_json="data2021.json", url_tag=12)
   company2020_list = get_data_global500("https://www.caifuzhongwen.com/fortune500/paiming/global500/2020_%e4%b8%96%e7%95%8c500%e5%bc%ba.htm", data_json="data2020.json", url_tag=10)
   
   for company in company2020_list:
       print("{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}\t{}".format( \
                company.rank,    company.industry,              company.company_name,company.company_name_en,       company.revenue, \
                company.country, company.employee,              company.revenue,     company.revenue_change_percent, \
                company.profit,  company.profit_change_percent, company.total_money, company.shareholders_equity,   company.ceo))
