import time
from selenium import webdriver

from Country import Country

def get_data(web_driver):
    try:
        table_class = web_driver.find_elements_by_class_name("el-table__body-wrapper")[0]
    except:
        print("[-]: Cannot find table class.")

    try:
        table_rows = table_class.find_elements_by_class_name("el-table__row")
    except:
        print("[-]: Cannot find table rows.")

    countries_list = []

    for country_index, table_row in enumerate(table_rows):
        country = Country()
        country.rank             = country_index
        country.name             = table_row.find_elements_by_xpath(".//td[1]/div[1]/a/span")[0].get_attribute("textContent") # For hidden Data
        country.conv19_new       = table_row.find_elements_by_xpath(".//td[2]/div[1]/span")[0].get_attribute("textContent")
        country.conv19_all       = table_row.find_elements_by_xpath(".//td[3]/div[1]/span")[0].get_attribute("textContent")
        country.conv19_current   = table_row.find_elements_by_xpath(".//td[4]/div[1]/span")[0].get_attribute("textContent")
        country.conv19_cure_new  = table_row.find_elements_by_xpath(".//td[5]/div[1]/span")[0].get_attribute("textContent")
        country.conv19_cure      = table_row.find_elements_by_xpath(".//td[6]/div[1]/span")[0].get_attribute("textContent")
        country.conv19_cure_rate = table_row.find_elements_by_xpath(".//td[7]/div[1]/span")[0].get_attribute("textContent")
        country.death_new        = table_row.find_elements_by_xpath(".//td[8]/div[1]/span")[0].get_attribute("textContent")
        country.death_all        = table_row.find_elements_by_xpath(".//td[9]/div[1]/span")[0].get_attribute("textContent")
        country.death_rate       = table_row.find_elements_by_xpath(".//td[10]/div[1]/span")[0].get_attribute("textContent")
        country.conv19_rate      = table_row.find_elements_by_xpath(".//td[11]/div[1]/span")[0].get_attribute("textContent")
        country.peoples          = table_row.find_elements_by_xpath(".//td[12]/div[1]/span")[0].get_attribute("textContent")
        country.peoples_density  = table_row.find_elements_by_xpath(".//td[13]/div[1]/span")[0].get_attribute("textContent")
        country.gdp              = table_row.find_elements_by_xpath(".//td[14]/div[1]/span")[0].get_attribute("textContent")
        country.gdp_per          = table_row.find_elements_by_xpath(".//td[15]/div[1]/span")[0].get_attribute("textContent")
        print(country.rank, country.name)
        countries_list.append(country)

    return countries_list


if __name__ == '__main__':
    url = 'https://www.zq-ai.com/#/fe/xgfybigdata'

    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    driver  = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(5)
    conv19_countries = get_data(driver)
