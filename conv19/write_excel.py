import time
import openpyxl
from selenium import webdriver

from get_data import get_data

def write_excel(country_list, out_file='result.xlsx'):

    wb = openpyxl.Workbook()
    ws        = wb.create_sheet(str("CONV19"))
    menu_row  = ['排名','国家','新增','累计确诊','现有确诊','新增治愈','累计治愈','治愈率(%)','新增死亡','累计死亡','死亡率(%)','感染率','人口(万人)','人口密度(平方千米)','GDP亿美元','人均GDP万美元']
    ws.append(menu_row)

    for country in country_list:
        country_line = [country.rank,
                        country.name,
                        country.conv19_new,
                        country.conv19_all,
                        country.conv19_current,
                        country.conv19_cure_new,
                        country.conv19_cure,
                        country.conv19_cure_rate,
                        country.death_new,
                        country.death_all,
                        country.death_rate,
                        country.conv19_rate,
                        country.peoples,
                        country.peoples_density,
                        country.gdp,
                        country.gdp_per]
        ws.append(country_line)

    wb.save(out_file)

    print("[+] Info: Write Excel Done!")

if __name__ == '__main__':
    url = 'https://www.zq-ai.com/#/fe/xgfybigdata'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver  = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)
    conv19_countries = get_data(driver)

    write_excel(conv19_countries)

