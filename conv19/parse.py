from urllib.request import urlopen
from lxml import etree
import requests
import openpyxl
from selenium import webdriver
import time

pandemic = {}

options = webdriver.ChromeOptions()
# options.add_argument('headless')
f = open("/home/sun/test.html", 'w')
driver  = webdriver.Chrome(options=options)
driver.get('https://www.zq-ai.com/#/fe/xgfybigdata')
time.sleep(5)
data = driver.find_element_by_xpath("//*").get_attribute("outerHTML")
# data = requests.get('https://www.zq-ai.com/#/fe/xgfybigdata', headers=header, verify=False, timeout=300).text.encode('iso-8859-1').decode('utf-8')
# print(data) 
f.write(data)
f.close()
exit()
s = etree.HTML(data)
data_path = s.xpath('/html/body/div/div/section[2]/section/main/div/div[6]/div[3]/table/tbody')[0]

for i in range(1,186):
    country_name = data_path.xpath('./tr[{}]/td[1]/div/a/text()'.format(i))[0]
    #new_quezheng = data_path.xpath('./tr[{}]/td[2]/div/text()'.format(i))[0]
    sum_quezheng = data_path.xpath('./tr[{}]/td[3]/div/text()'.format(i))[0]
    now_quezheng = data_path.xpath('./tr[{}]/td[4]/div/text()'.format(i))[0]
    sum_zhiyu = data_path.xpath('./tr[{}]/td[6]/div/text()'.format(i))[0]
    rate_zhiyu = data_path.xpath('./tr[{}]/td[7]/div/text()'.format(i))[0]
    sum_siwang = data_path.xpath('./tr[{}]/td[9]/div/text()'.format(i))[0]
    rate_siwang = data_path.xpath('./tr[{}]/td[10]/div/text()'.format(i))[0]
    try:
        rate_ganran = data_path.xpath('./tr[{}]/td[11]/div/text()'.format(i))[0]
    except:
        rate_ganran = ''
    try:
        population = data_path.xpath('./tr[{}]/td[12]/div/text()'.format(i))[0]
    except:
        population = ''
    try:
        population_midu = data_path.xpath('./tr[{}]/td[13]/div/text()'.format(i))[0]
    except:
        population_midu = ''
    try:
        GDP = data_path.xpath('./tr[{}]/td[14]/div/text()'.format(i))[0]
    except:
        GDP = ''
    try:
        GPD_person = data_path.xpath('./tr[{}]/td[15]/div/text()'.format(i))[0]
    except:
        GPD_person = ''

    pandemic.update({country_name:[sum_quezheng,now_quezheng,sum_zhiyu,rate_zhiyu,sum_siwang,rate_siwang,rate_ganran,population,population_midu,GDP,GPD_person]})

wb = openpyxl.Workbook()
ws = wb.create_sheet('whpj')
menu_row = ['','','国家','累计确诊','现有确诊','累计治愈','治愈率','累计死亡','死亡率','感染率','人口','人口密度','GDP','人均GDP']
ws.append(menu_row)

for key in pandemic:
    data = ['','',pandemic[key][0],pandemic[key][1],pandemic[key][2],pandemic[key][3],pandemic[key][4],pandemic[key][5],pandemic[key][6],pandemic[key][7],pandemic[key][8],pandemic[key][9],pandemic[key][10]]
    ws.append(data)

wb.save('pandemic.xlsx')